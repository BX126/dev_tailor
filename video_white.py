from manim import *
import numpy as np

class PhysicalWorldModel(Scene):
    def construct(self):
        # 1. Colors & Configuration (Inverted for White Background)
        head_color, tail_color = BLUE_D, ORANGE
        text_color = BLACK
        desc_color = "#333333" # Dark grey for readability
        self.camera.background_color = "#FFFFFF"

        # 2. Opening Statement
        intro_text = Text(
            "Physical interactions follow a long-tailed distribution.", 
            font_size=36, color=text_color
        ).to_edge(UP, buff=0.8)
        self.play(Write(intro_text))

        self.play(intro_text.animate.scale(0.8).to_edge(UP, buff=0.5))
        self.play(intro_text.animate.set_color_by_gradient(BLUE_E, ORANGE))
        
        # 3. Setup Axes & Labels
        axes = Axes(
            x_range=[0, 10, 1], y_range=[0, 1, 0.2],
            axis_config={
                "color": text_color,
                "include_tip": True,
                "stroke_width": 2
            },
            x_length=10, y_length=3.6,
        ).to_edge(DOWN, buff=0.5)

        x_label = Text("Physical Interaction Space", font_size=20, color=text_color).next_to(axes.x_axis, DOWN).shift(UP * 0.12)
        y_label = Text("Frequency", font_size=20, color=text_color).rotate(90*DEGREES).next_to(axes.y_axis, LEFT).shift(UP * 0.12)

        curve = axes.plot(
            lambda x: 0.8 * np.exp(-1.5 * x) + 0.1 / (x + 0.5), 
            x_range=[0, 9.5], color=text_color
        ).shift(UP * 0.12)

        self.play(Write(axes), Write(x_label), Write(y_label))
        self.play(Create(curve))

        # 4. Head Scenario
        hammer_head = Rectangle(width=0.5, height=0.25, fill_opacity=1, color=GRAY_E)
        hammer_handle = Rectangle(width=0.1, height=0.6, fill_opacity=1, color="#5D2906").next_to(hammer_head, DOWN, buff=0)
        hammer = VGroup(hammer_head, hammer_handle).scale(0.7).move_to(axes.c2p(1, 0.6))
        
        head_tag = Text(
            "Head\nScenarios", color=head_color, font_size=32, line_spacing=0.8
        ).next_to(hammer, RIGHT, buff=0.3)
        
        head_desc = Text(
            "Common interactions, such as using a hammer to crack a walnut,\ndominate both human experience and large-scale visual data.\nThese frequent and familiar cases form the head of the distribution,\nwhich we refer to as head scenarios.",
            font_size=22,
            color=desc_color,
            line_spacing=1.4,
            t2w={"Common interactions": BOLD},
            t2s={"head scenarios": ITALIC},
        ).to_edge(UP, buff=1.5).shift(RIGHT * 0.5)

        head_area = axes.get_area(curve, x_range=[0, 1.5], color=head_color, opacity=0.3)

        self.play(FadeIn(head_area), FadeIn(hammer), Write(head_tag))
        self.play(Write(head_desc))
        self.wait(4)

        # 5. Long-Tail Scenario Transition
        book_rect = Rectangle(width=0.45, height=0.6, fill_opacity=1, color=tail_color)
        # Spine line changed to WHITE for contrast against ORANGE book cover
        book_spine = Line(UP*0.3, DOWN*0.3, color=WHITE).move_to(book_rect.get_left() + RIGHT*0.1)
        book = VGroup(book_rect, book_spine).scale(0.8).move_to(axes.c2p(6.5, 0.3))
        
        tail_tag = Text(
            "Long-Tail\nScenarios", color=tail_color, font_size=32, line_spacing=0.8
        ).next_to(book, RIGHT, buff=0.3)
        
        tail_desc = Text(
            "Irregular interactions, such as using a hardcover book to crack a walnut,\nare rarely observed individually but collectively occupy a vast space of \nphysically valid possibilities. We refer to these cases as long-tail scenarios.",
            font_size=22,
            color=desc_color,
            line_spacing=1.4,
            t2w={"Irregular interactions": BOLD},
            t2s={"long-tail scenarios": ITALIC},
        ).move_to(head_desc.get_center())

        tail_area = axes.get_area(curve, x_range=[1.5, 9.5], color=tail_color, opacity=0.3)

        self.play(
            FadeOut(head_desc),
            ReplacementTransform(head_area, tail_area),
            ReplacementTransform(hammer, book),
            ReplacementTransform(head_tag, tail_tag),
            run_time=4
        )
        self.play(Write(tail_desc))
        self.play(Indicate(book, color=tail_color))
        self.wait(4)