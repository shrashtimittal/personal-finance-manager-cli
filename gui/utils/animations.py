from PySide6.QtCore import (
    QPropertyAnimation,
    QEasingCurve,
    QPoint,
    QObject
)


class PageTransition(QObject):
    """
    Handles smooth transitions between QStackedWidget pages.
    Designed to be lightweight and optional.
    """

    def __init__(self, stacked_widget):
        super().__init__()
        self.stack = stacked_widget
        self.duration = 220  # milliseconds

    # ===============================
    # FADE TRANSITION
    # ===============================
    def fade_to(self, index: int):
        current = self.stack.currentWidget()
        next_widget = self.stack.widget(index)

        if current == next_widget:
            return

        # Fade out current
        fade_out = QPropertyAnimation(current, b"windowOpacity")
        fade_out.setDuration(self.duration)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)
        fade_out.setEasingCurve(QEasingCurve.OutCubic)

        def switch_and_fade_in():
            self.stack.setCurrentIndex(index)
            next_widget.setWindowOpacity(0.0)

            fade_in = QPropertyAnimation(next_widget, b"windowOpacity")
            fade_in.setDuration(self.duration)
            fade_in.setStartValue(0.0)
            fade_in.setEndValue(1.0)
            fade_in.setEasingCurve(QEasingCurve.InCubic)
            fade_in.start(QPropertyAnimation.DeleteWhenStopped)

        fade_out.finished.connect(switch_and_fade_in)
        fade_out.start(QPropertyAnimation.DeleteWhenStopped)

    # ===============================
    # SLIDE TRANSITION
    # ===============================
    def slide_to(self, index: int, direction: str = "left"):
        current = self.stack.currentWidget()
        next_widget = self.stack.widget(index)

        if current == next_widget:
            return

        width = self.stack.frameRect().width()

        offset = {
            "left": QPoint(width, 0),
            "right": QPoint(-width, 0)
        }.get(direction, QPoint(width, 0))

        next_widget.move(offset)
        next_widget.show()

        anim_current = QPropertyAnimation(current, b"pos")
        anim_next = QPropertyAnimation(next_widget, b"pos")

        anim_current.setDuration(self.duration)
        anim_next.setDuration(self.duration)

        anim_current.setStartValue(current.pos())
        anim_current.setEndValue(QPoint(-offset.x(), 0))

        anim_next.setStartValue(offset)
        anim_next.setEndValue(QPoint(0, 0))

        anim_current.setEasingCurve(QEasingCurve.OutCubic)
        anim_next.setEasingCurve(QEasingCurve.OutCubic)

        def on_finished():
            self.stack.setCurrentIndex(index)
            current.move(0, 0)

        anim_current.finished.connect(on_finished)

        anim_current.start(QPropertyAnimation.DeleteWhenStopped)
        anim_next.start(QPropertyAnimation.DeleteWhenStopped)
