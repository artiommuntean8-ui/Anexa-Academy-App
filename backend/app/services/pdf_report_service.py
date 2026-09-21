"""Minimal PDF report generator (no extra runtime dependency)."""
from __future__ import annotations

import io
import logging
from datetime import datetime
from typing import Dict

logger = logging.getLogger("app.services.pdf_report")


def _escape(text: str) -> str:
    return (
        (text or "")
        .replace("\\", "\\\\")
        .replace("(", "\\(")
        .replace(")", "\\)")
    )


def _latin(text: str) -> str:
    return (text or "").encode("latin-1", "replace").decode("latin-1")


class ReportPDF:
    """Builds a simple one-page student progress PDF."""

    def generate_report(
        self,
        student_name: str,
        xp: int,
        level: int,
        progress_pct: float,
        modules: Dict[str, str],
    ) -> bytes:
        try:
            lines = [
                "Anexa Academy — Raport de progres",
                f"Generat: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
                "",
                f"Elev: {_latin(student_name)}",
                f"XP: {int(xp)}",
                f"Nivel: {int(level)}",
                f"Progres general: {progress_pct}%",
                "",
                "Module:",
            ]
            if modules:
                for name, status in modules.items():
                    lines.append(f"  - {_latin(str(name))}: {_latin(str(status))}")
            else:
                lines.append("  (niciun modul inrolat)")

            y = 780
            content_ops = ["BT", "/F1 16 Tf", "50 800 Td", f"({_escape(lines[0])}) Tj", "ET"]
            y = 770
            for line in lines[1:]:
                content_ops.extend(
                    ["BT", "/F1 11 Tf", f"50 {y} Td", f"({_escape(line)}) Tj", "ET"]
                )
                y -= 18
                if y < 60:
                    break
            stream = "\n".join(content_ops).encode("latin-1", "replace")

            objects = []
            objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
            objects.append(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
            objects.append(
                b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
                b"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>"
            )
            objects.append(b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream")
            objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

            buf = io.BytesIO()
            buf.write(b"%PDF-1.4\n")
            offsets = [0]
            for i, obj in enumerate(objects, start=1):
                offsets.append(buf.tell())
                buf.write(f"{i} 0 obj\n".encode("ascii"))
                buf.write(obj)
                buf.write(b"\nendobj\n")
            xref_pos = buf.tell()
            buf.write(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
            buf.write(b"0000000000 65535 f \n")
            for off in offsets[1:]:
                buf.write(f"{off:010d} 00000 n \n".encode("ascii"))
            buf.write(
                f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode(
                    "ascii"
                )
            )
            return buf.getvalue()
        except Exception as e:
            logger.error(f"Error generating PDF report: {e}")
            raise ValueError(f"Eroare la generarea raportului PDF: {str(e)}")
