import pygal


class GraphSettings():
    def __init__(self):
        self.config = pygal.Config(
            show_legend=False,
            x_label_rotation=45,
            title=f"Untitled"
        )
        self.style = pygal.style.Style(
            label_font_size=8
        )
