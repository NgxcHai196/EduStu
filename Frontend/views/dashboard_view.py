from __future__ import annotations
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QFrame, QGridLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from views.base_view import BaseView
from controllers.report import ReportController
from utils.config import SECONDARY, BORDER, TEXT_LIGHT, TEXT_MUTED, SUCCESS, WARNING, DANGER, INFO, HIGHLIGHT


class StatCard(QFrame):
    def __init__(self, label: str, value: str, color: str):
        super().__init__()
        self.setStyleSheet(f"""
            QFrame {{
                background: #FFFFFF;
                border: none;
                border-top: 4px solid {color};
                border-radius: 16px;
            }}
        """)
        from PyQt6.QtWidgets import QGraphicsDropShadowEffect
        from PyQt6.QtGui import QColor as _C
        sh = QGraphicsDropShadowEffect(self)
        sh.setBlurRadius(24); sh.setOffset(0, 5)
        sh.setColor(_C(0, 0, 0, 55))
        self.setGraphicsEffect(sh)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 18, 22, 18)
        layout.setSpacing(4)
        lbl = QLabel(label)
        lbl.setStyleSheet("color:#64748B;font-size:13px;font-family:Roboto;border:none;")
        val = QLabel(value)
        val.setFont(QFont("Roboto", 30, QFont.Weight.Bold))
        val.setStyleSheet(f"color:{color};border:none;")
        layout.addWidget(lbl)
        layout.addWidget(val)
        self._val = val

    def set_value(self, v: str):
        self._val.setText(v)


class DashboardView(BaseView):
    PAGE_TITLE = "Dashboard"
    PAGE_SUB   = "Tổng quan hệ thống"

    def __init__(self):
        self._ctrl = ReportController()
        super().__init__()

    def build_ui(self):
        # Stat cards
        self._grid = QGridLayout()
        self._grid.setSpacing(12)
        colors = [INFO, SUCCESS, WARNING, DANGER]
        labels = ["Tổng sinh viên", "Đang học", "Cảnh báo học vụ", "Nợ học phí"]
        self._cards = []
        for i, (lbl, clr) in enumerate(zip(labels, colors)):
            c = StatCard(lbl, "—", clr)
            self._cards.append(c)
            self._grid.addWidget(c, 0, i)
        self._root.addLayout(self._grid)

        # Alerts panel
        self._alert_frame = QFrame()
        self._alert_frame.setStyleSheet(f"""
            QFrame {{
                background: #FFFFFF;
                border: none;
                border-top: 4px solid {DANGER};
                border-radius: 16px;
            }}
        """)
        from PyQt6.QtWidgets import QGraphicsDropShadowEffect
        from PyQt6.QtGui import QColor as _QColor
        sh2 = QGraphicsDropShadowEffect(self._alert_frame)
        sh2.setBlurRadius(18); sh2.setOffset(0, 3)
        sh2.setColor(_QColor(0, 0, 0, 25))
        self._alert_frame.setGraphicsEffect(sh2)
        al = QVBoxLayout(self._alert_frame)
        al.setContentsMargins(20, 16, 20, 16)
        al.setSpacing(8)
        title = QLabel("Cảnh báo gần đây")
        title.setFont(QFont("Roboto", 14, QFont.Weight.Bold))
        title.setStyleSheet("color:#0F172A;border:none;")
        al.addWidget(title)
        self._alert_layout = QVBoxLayout()
        self._alert_layout.setSpacing(6)
        al.addLayout(self._alert_layout)
        self._root.addWidget(self._alert_frame)
        self._root.addStretch()

    def refresh(self):
        self.run_async(self._ctrl._svc.get_dashboard, self._render)

    def _render(self, data: dict):
        vals = [
            str(data.get("tong_sv", 0)),
            str(data.get("dang_hoc", 0)),
            str(data.get("canh_bao_hv", 0)),
            str(data.get("no_hoc_phi", 0)),
        ]
        for card, val in zip(self._cards, vals):
            card.set_value(val)

        while self._alert_layout.count():
            item = self._alert_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        alerts = data.get("alerts", [])
        if not alerts:
            lbl = QLabel("Không có cảnh báo nào.")
            lbl.setStyleSheet("color:#94A3B8;font-size:13px;font-family:Roboto;border:none;")
            self._alert_layout.addWidget(lbl)
        for a in alerts[:6]:
            row = QFrame()
            row.setStyleSheet(f"""
                QFrame {{
                    background: #FEF2F2;
                    border-radius: 10px;
                    border: 1px solid #FECACA;
                }}
            """)
            rl = QHBoxLayout(row)
            rl.setContentsMargins(12, 8, 12, 8)
            dot = QLabel("●")
            dot.setStyleSheet(f"color:{DANGER};font-size:9px;border:none;")
            lbl = QLabel(f"<b>{a.get('ho_ten','')}</b> — {a.get('mo_ta','')}")
            lbl.setStyleSheet(f"color:#1E293B;font-size:13px;font-family:Roboto;border:none;")
            rl.addWidget(dot)
            rl.addWidget(lbl)
            self._alert_layout.addWidget(row)