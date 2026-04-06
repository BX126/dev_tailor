import argparse
import json
import os
import sys
from functools import partial
from multiprocessing import Pool, cpu_count
from typing import Any, Dict, List

sys.path.append(os.path.dirname(__file__))

from s6_rubric_generation import (  # type: ignore[import]
    generate_rubric_for_evaluation_instance,
)


def _load_tasks(input_path: str) -> Any:
    with open(input_path, "r") as f:
        data = json.load(f)

    if isinstance(data, dict) and "tasks" in data:
        tasks = data["tasks"]
    else:
        tasks = data

    if not isinstance(tasks, list):
        raise ValueError("Expected a list of task objects or a dict with 'tasks' key.")

    return data, tasks


def _wrap_tasks(original_data: Any, augmented_tasks: List[Dict[str, Any]]) -> Any:
    if isinstance(original_data, dict) and "tasks" in original_data:
        out_data: Any = dict(original_data)
        out_data["tasks"] = augmented_tasks
    else:
        out_data = augmented_tasks
    return out_data


def _process_single_task(task: Dict[str, Any]) -> Dict[str, Any]:
    """Generate rubrics for all evaluation_instances in a single task."""
    eval_instances = task.get("evaluation_instances", [])
    new_eval_instances = [
        generate_rubric_for_evaluation_instance(task, ei) for ei in eval_instances
    ]
    new_task = dict(task)
    new_task["evaluation_instances"] = new_eval_instances
    return new_task


def generate_rubrics_for_file_parallel(
    input_path: str, output_path: str, num_workers: int = 10
) -> List[Dict[str, Any]]:
    """Parallel version of rubric generation using a worker pool over tasks."""
    original_data, tasks = _load_tasks(input_path)

    if num_workers <= 0:
        num_workers = 1
    else:
        num_workers = min(num_workers, cpu_count(), len(tasks))

    print(
        f"Generating rubrics for {len(tasks)} tasks "
        f"with {num_workers} parallel workers..."
    )

    with Pool(processes=num_workers) as pool:
        process_func = partial(_process_single_task)
        augmented_tasks = pool.map(process_func, tasks)

    out_data = _wrap_tasks(original_data, augmented_tasks)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(out_data, f, indent=4, ensure_ascii=False)

    total_instances = sum(
        len(t.get("evaluation_instances", [])) for t in augmented_tasks
    )
    print(
        f"Generated rubrics for {total_instances} evaluation instances "
        f"across {len(augmented_tasks)} tasks."
    )
    print(f"Saved augmented tasks with rubrics to: {output_path}")

    return augmented_tasks


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run Step 6 rubric generation in parallel over tasks."
    )
    parser.add_argument(
        "-j",
        "--jobs",
        type=int,
        default=10,
        help="Number of parallel workers (default: 10).",
    )
    parser.add_argument(
        "--input",
        type=str,
        default=None,
        help=(
            "Path to input JSON (default: tasks/selected_tasks_with_prompts.json "
            "relative to this script)."
        ),
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help=(
            "Path to output JSON (default: tasks/selected_tasks_with_rubrics.json "
            "relative to this script)."
        ),
    )
    args = parser.parse_args()

    base_dir = os.path.dirname(__file__)
    tasks_dir = os.path.join(base_dir, "..", "tasks")

    input_path = args.input or os.path.join(
        tasks_dir, "selected_tasks_with_prompts.json"
    )
    output_path = args.output or os.path.join(
        tasks_dir, "selected_tasks_with_rubrics.json"
    )

    print(f"Loading tasks with prompts from: {input_path}")
    if not os.path.exists(input_path):
        raise FileNotFoundError(
            f"Input file not found: {input_path}. "
            "Run s5_prompt_generation.py first to create it."
        )

    generate_rubrics_for_file_parallel(
        input_path=input_path, output_path=output_path, num_workers=args.jobs
    )


if __name__ == "__main__":
    main()

