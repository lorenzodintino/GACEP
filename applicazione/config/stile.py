class ColoriCSS:
    def __init__(self):
        pass

    def success_background(self):
        return """rgba(33, 195, 84, 0.12)"""

    def success_label(self):
        return """#177233"""

    def success(self):
        return f"""
        background-color: {self.success_background()};
        color: {self.success_label()};
        """

    def error_background(self):
        return """rgba(255, 43, 43, 0.09)"""

    def error_label(self):
        return """#7d353b"""

    def error(self):
        return f"""
        background-color: {self.error_background()};
        color: {self.error_label()};
        """

    def warning_background(self):
        return """rgba(255, 227, 18, 0.1)"""

    def warning_label(self):
        return """#926c05"""

    def warning(self):
        return f"""
        background-color: {self.warning_background()};
        color: {self.warning_label()};
        """
