from manim import *
import numpy as np

class LongTailComparison(Scene):
    def construct(self):
        # 1. Colors & Configuration
        head_color, tail_color = BLUE_D, ORANGE
        text_color = BLACK
        desc_color = "#333333"
        self.camera.background_color = "#FFFFFF"

        # 2. Setup Axes
        axes = Axes(
            x_range=[0, 10, 1], y_range=[0, 1, 0.2],
            axis_config={"color": text_color, "include_tip": True, "stroke_width": 2},
            x_length=10, y_length=5,
        ).to_edge(DOWN, buff=0.5).shift(UP*0.2)

        x_label = Text("Physical Interaction Space", font_size=20, color=text_color).next_to(axes.x_axis, DOWN).shift(UP*0.2)
        y_label = Text("Frequency", font_size=20, color=text_color).next_to(axes.y_axis, LEFT).shift(UP*0.2)
        
        curve = axes.plot(
            lambda x: 0.8 * np.exp(-1.2 * x) + 0.05, 
            x_range=[0, 9.5], color=text_color
        )

        header = Text(
            "Physical interactions follow a long-tail distribution", 
            font_size=32, color=text_color
        ).to_edge(UP, buff=0.5)
        
        self.play(Write(header),Write(axes), Write(x_label), Write(y_label))
        self.play(Create(curve))

        # --- HEAD SCENARIO ---
        head_area = axes.get_area(curve, x_range=[0, 1.5], color=head_color, opacity=0.3)
        
        # Tool Icon (Screwdriver)
        tool_icon = Square(side_length=0.35, fill_opacity=1, color=BLUE_E).next_to(head_area, RIGHT, buff=0.02)

        head_label = Text("Regular and Common Interactions\n\t\t\t(Head-Scenarios)", color=head_color, font_size=24).next_to(head_area, RIGHT, buff=0.5)

        self.play(FadeIn(head_area), FadeIn(tool_icon), Write(head_label))
        self.wait(1)


        # --- TRANSITION TO LONG TAIL ---
        new_header = Text(
            "Success in head scenarios may rely on co-occurrence matching,\nbut long-tail scenarios require reasoning about physical principles.",
            font_size=28,
            color=text_color,
            line_spacing=1.0,
            t2w={"head scenarios": BOLD, "long-tail scenarios": BOLD}
        ).to_edge(UP, buff=0.5)

        tail_area = axes.get_area(curve, x_range=[1.5, 9.5], color=tail_color, opacity=0.3)
        
        # Unstructured Object
        unstructured_obj = Polygon(
            [-0.2, -0.1, 0], [0.2, -0.2, 0], [0.3, 0.3, 0], [-0.1, 0.4, 0], [-0.3, 0.1, 0],
            color=tail_color, fill_opacity=1
        ).scale(0.7).next_to(tail_area, UP, buff=0.9)
        

        tail_label = Text("Irregular and Rare Interactions\n\t\t(Long-Tailed Scenarios)", color=tail_color, font_size=24).next_to(tail_area, UP, buff=0.2)

        self.play(
            ReplacementTransform(head_area, tail_area),
            ReplacementTransform(tool_icon, unstructured_obj),
            FadeOut(head_label),
            Write(tail_label),
            run_time=1.5
        )
        self.wait(1)
        self.play(Transform(header, new_header))
        self.wait(1)
        
        # explanation = Text(
        #     "Pattern recognition fails where data is sparse.\nGeneralization requires physical reasoning.",
        #     font_size=20, color=desc_color, line_spacing=1.2
        # ).next_to(new_header, DOWN, buff=0.3)
        
        # self.play(FadeIn(explanation))
        
        gap_line = DashedLine(
            axes.c2p(1.5, 0), axes.c2p(1.5, 1), color=RED, stroke_width=3
        )
        gap_text = Text("The Long-Tail of World Modeling", color=RED, font_size=22).next_to(gap_line, UP, buff=0.1)
        
        self.play(Create(gap_line), Write(gap_text))
        self.play(Indicate(gap_text, scale_factor=1.1))
        self.wait(1)

        final_title = Text(
            "We focus on the long-tail of world modeling that is\nlargely overlooked in current world model evaluations", 
            font_size=28,
            color=text_color,
            line_spacing=1,
            t2w={"the long-tail of world modeling": BOLD}
        ).to_edge(UP, buff=0.5)
        self.play(Transform(header, final_title))
        self.play(final_title.animate.set_color_by_gradient(BLUE, ORANGE))
        self.wait(3)