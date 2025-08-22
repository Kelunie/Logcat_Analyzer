import re
from datetime import datetime
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
from tkinter import Tk, Frame, Button, PhotoImage
from PIL import Image, ImageTk, ImageDraw


def resource_path(relative_path):
    """Obtiene la ruta absoluta para recursos, funciona también en PyInstaller."""
    try:
        base_path = sys._MEIPASS  # PyInstaller crea esta carpeta temporal
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, color, text_color, hover_color, corner_radius,
                 command=None, icon_path=None, icon_size=(20, 20),
                 width=200, height=50, font=("Arial", 12)):
        super().__init__(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0)

        self.command = command
        self.color = color
        self.hover_color = hover_color
        self.corner_radius = corner_radius
        self.width = width
        self.height = height
        self.font = font

        # Fondo redondeado
        self.rounded_rect = self.create_rounded_rect(0, 0, width, height, corner_radius, fill=color, outline=color)

        # Contenedor centrado
        content_frame = tk.Frame(self, bg=color)
        self.create_window(width // 2, height // 2, window=content_frame, anchor="center")

        # Si hay icono, lo añadimos
        if icon_path:
            img = Image.open(icon_path).resize(icon_size, Image.LANCZOS)
            self.icon = ImageTk.PhotoImage(img)
            tk.Label(content_frame, image=self.icon, bg=color).pack(side="left", padx=5)

        # Texto centrado con fuente configurable
        self.text_label = tk.Label(
            content_frame,
            text=text,
            fg=text_color,
            bg=color,
            font=self.font,
            anchor="center"
        )
        self.text_label.pack(side="left", padx=5)

        # Eventos hover y click
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        self.bind("<ButtonRelease-1>", self.on_release)

    def create_rounded_rect(self, x1, y1, x2, y2, r=25, **kwargs):
        """Dibuja un rectángulo redondeado"""
        points = [
            x1 + r, y1,
            x1 + r, y1,
            x2 - r, y1,
            x2 - r, y1,
            x2, y1,
            x2, y1 + r,
            x2, y1 + r,
            x2, y2 - r,
            x2, y2 - r,
            x2, y2,
            x2 - r, y2,
            x2 - r, y2,
            x1 + r, y2,
            x1 + r, y2,
            x1, y2,
            x1, y2 - r,
            x1, y2 - r,
            x1, y1 + r,
            x1, y1 + r,
            x1, y1,
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def on_enter(self, event):
        self.itemconfig(self.rounded_rect, fill=self.hover_color, outline=self.hover_color)

    def on_leave(self, event):
        self.itemconfig(self.rounded_rect, fill=self.color, outline=self.color)

    def on_click(self, event):
        # oscurecer un poco al hacer click
        darker = self.darken_color(self.color)
        self.itemconfig(self.rounded_rect, fill=darker, outline=darker)

    def on_release(self, event):
        self.itemconfig(self.rounded_rect, fill=self.hover_color, outline=self.hover_color)
        if self.command:
            self.command()

    def darken_color(self, color):
        """Oscurecer ligeramente el color para el efecto de click"""
        if color.startswith('#'):
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            r = max(0, r - 30)
            g = max(0, g - 30)
            b = max(0, b - 30)
            return f'#{r:02x}{g:02x}{b:02x}'
        return color


class LogAnalyzer:
    def __init__(self):
        self.wifi_patterns = {
            'wifi_connection': r'CONNECTIVITY_CHANGE|WifiService|wpa_supplicant|wlan0',
            'wifi_scan': r'scan|SCAN|Scan',
            'wifi_error': r'failed|error|timeout|not found|disconnect|Wifi.*error',
            'network_state': r'NETWORK|network|internet|online|offline'
        }

        self.system_patterns = {
            'crash': r'FATAL EXCEPTION|crash|died|has died',
            'error': r'ERROR|Error|E\/|Exception|NullPointerException',
            'warning': r'WARNING|Warning|W\/',
            'slow_operation': r'Slow operation|slow dispatch|slow delivery',
            'boot': r'BOOT_COMPLETED|boot|startup'
        }

        self.results = {
            'wifi_events': [],
            'network_events': [],
            'system_issues': [],
            'timeline': []
        }

    def analyze_line(self, line):
        """Analiza una línea del log y clasifica la información"""
        timestamp = self.extract_timestamp(line)
        if not timestamp:
            return None

        category = None
        event_type = None

        # Verificar patrones de WiFi
        for pattern_type, pattern in self.wifi_patterns.items():
            if re.search(pattern, line, re.IGNORECASE):
                if 'wifi' in pattern_type:
                    category = 'wifi'
                    event_type = pattern_type
                else:
                    category = 'network'
                    event_type = pattern_type
                break

        # Verificar patrones del sistema
        if not category:
            for pattern_type, pattern in self.system_patterns.items():
                if re.search(pattern, line, re.IGNORECASE):
                    category = 'system'
                    event_type = pattern_type
                    break

        if category:
            return {
                'timestamp': timestamp,
                'category': category,
                'type': event_type,
                'message': line.strip(),
                'raw_line': line
            }

        return None

    def extract_timestamp(self, line):
        """Extrae el timestamp de una línea de log"""
        timestamp_match = re.match(r'(\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})', line)
        if timestamp_match:
            return timestamp_match.group(1)
        return None

    def parse_log_file(self, filename):
        """Parsea el archivo de log completo"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                for line in file:
                    analyzed = self.analyze_line(line)
                    if analyzed:
                        self.classify_event(analyzed)
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {filename}")
            return False
        except UnicodeDecodeError:
            print("Error: Problema de codificación del archivo")
            return False

        return True

    def classify_event(self, event):
        """Clasifica el evento en la categoría correspondiente"""
        if event['category'] == 'wifi':
            self.results['wifi_events'].append(event)
        elif event['category'] == 'network':
            self.results['network_events'].append(event)
        elif event['category'] == 'system':
            self.results['system_issues'].append(event)

        self.results['timeline'].append(event)

    def generate_report(self):
        """Genera un reporte completo del análisis"""
        report = []

        # Resumen estadístico
        wifi_count = len(self.results['wifi_events'])
        network_count = len(self.results['network_events'])
        system_count = len(self.results['system_issues'])

        report.append("=" * 80)
        report.append("ANÁLISIS DE LOGS - CONECTIVIDAD Y SISTEMA")
        report.append("=" * 80)
        report.append(f"Eventos WiFi detectados: {wifi_count}")
        report.append(f"Eventos de red detectados: {network_count}")
        report.append(f"Problemas del sistema detectados: {system_count}")
        report.append("")

        # Eventos de WiFi
        if wifi_count > 0:
            report.append("EVENTOS DE WiFi:")
            report.append("-" * 80)
            for event in self.results['wifi_events']:
                report.append(f"{event['timestamp']} - {event['type']}: {event['message'][:100]}...")
            report.append("")

        # Problemas del sistema
        if system_count > 0:
            report.append("PROBLEMAS DEL SISTEMA:")
            report.append("-" * 80)
            for event in self.results['system_issues']:
                if 'error' in event['type'].lower() or 'crash' in event['type'].lower():
                    report.append(f"❌ {event['timestamp']} - {event['type']}: {event['message'][:120]}...")
                elif 'warning' in event['type'].lower():
                    report.append(f"⚠️  {event['timestamp']} - {event['type']}: {event['message'][:100]}...")
            report.append("")

        # Timeline cronológico
        report.append("LINEA DE TIEMPO (primeros 10 eventos):")
        report.append("-" * 80)
        for event in self.results['timeline'][:10]:
            emoji = "📶" if event['category'] == 'wifi' else "🌐" if event['category'] == 'network' else "💥"
            report.append(f"{emoji} {event['timestamp']} - {event['category']}/{event['type']}")

        return "\n".join(report)

    def get_detailed_wifi_info(self):
        """Obtiene información detallada sobre eventos WiFi"""
        wifi_details = []

        connections = [e for e in self.results['wifi_events'] if 'connection' in e['type']]
        scans = [e for e in self.results['wifi_events'] if 'scan' in e['type']]
        errors = [e for e in self.results['wifi_events'] if 'error' in e['type']]

        wifi_details.append("DETALLES DE CONECTIVIDAD WiFi:")
        wifi_details.append(f"  • Conexiones establecidas: {len(connections)}")
        wifi_details.append(f"  • Escaneos realizados: {len(scans)}")
        wifi_details.append(f"  • Errores de WiFi: {len(errors)}")

        if errors:
            wifi_details.append("  • Último error:")
            wifi_details.append(f"    {errors[-1]['message'][:150]}")

        return "\n".join(wifi_details)

    def generate_errors_table_text(self, errors):
        """Genera texto formateado para la tabla de errores"""
        if not errors:
            return "No se encontraron errores del sistema.\n"

        table_text = []
        table_text.append("=" * 120)
        table_text.append("TABLA DE ERRORES DEL SISTEMA")
        table_text.append("=" * 120)
        table_text.append(f"{'Timestamp':<20} {'Tipo':<15} {'Mensaje':<80}")
        table_text.append("-" * 120)

        for err in errors:
            timestamp = err['timestamp']
            error_type = err['type']
            message = err['message'][:75] + "..." if len(err['message']) > 75 else err['message']
            table_text.append(f"{timestamp:<20} {error_type:<15} {message:<80}")

        table_text.append("=" * 120)
        table_text.append(f"Total de errores encontrados: {len(errors)}")
        return "\n".join(table_text)


def save_to_file(content, filename):
    """Guarda contenido en un archivo TXT"""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        return True
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el archivo: {str(e)}")
        return False


def show_errors_table(errors, analyzer_instance):
    """Muestra la tabla de errores y guarda archivo TXT"""
    if not errors:
        return

    # Generar texto para el archivo usando la instancia de analyzer
    table_text = analyzer_instance.generate_errors_table_text(errors)

    # Guardar archivo de tabla
    table_filename = f"errores_sistema_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    if save_to_file(table_text, table_filename):
        messagebox.showinfo("Archivo guardado", f"Tabla de errores guardada como: {table_filename}")

    # Mostrar ventana con la tabla
    table_window = tk.Toplevel()
    table_window.iconbitmap(resource_path("img/icon.ico"))
    table_window.title("System Errors")
    table_window.geometry("700x400")

    style = ttk.Style(table_window)
    style.configure("Treeview.Heading", anchor="center")
    style.configure("Treeview", rowheight=28, borderwidth=2, relief="solid")
    style.map("Treeview", background=[("selected", "#ececec")])

    columns = ("Timestamp", "Type", "Message")
    tree = ttk.Treeview(table_window, columns=columns, show="headings", style="Treeview")
    for col in columns:
        tree.heading(col, text=col, anchor="center")
        tree.column(col, anchor="center", width=150 if col != "Message" else 300, stretch=True)

    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    for err in errors:
        tree.insert("", "end", values=(err['timestamp'], err['type'], err['message'][:80]))


def show_report_ui(report, wifi_details, analyzer_instance):
    """Muestra el reporte y guarda archivo TXT"""
    # Guardar archivo de reporte completo
    full_report = report + "\n\n" + wifi_details
    report_filename = f"reporte_analisis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    if save_to_file(full_report, report_filename):
        messagebox.showinfo("Archivo guardado", f"Reporte completo guardado como: {report_filename}")

    # Mostrar ventana con el reporte
    report_window = tk.Toplevel()
    report_window.iconbitmap(resource_path("img/icon.ico"))
    report_window.title("Logcat Analysis Report")
    report_window.geometry("700x600")

    text_area = scrolledtext.ScrolledText(report_window, wrap=tk.WORD, font=("Consolas", 10))
    text_area.pack(fill=tk.BOTH, expand=True)
    text_area.insert(tk.END, full_report)
    text_area.config(state=tk.DISABLED)


def analyze_log_file():
    filename = filedialog.askopenfilename(
        title="Seleccione el archivo de logs",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filename:
        return

    analyzer = LogAnalyzer()
    if analyzer.parse_log_file(filename):
        report = analyzer.generate_report()
        wifi_details = analyzer.get_detailed_wifi_info()

        show_report_ui(report, wifi_details, analyzer)

        errors = [e for e in analyzer.results['system_issues'] if
                  'error' in e['type'].lower() or 'crash' in e['type'].lower()]
        if errors:
            show_errors_table(errors, analyzer)
            messagebox.showinfo("Errores encontrados",
                                f"{len(errors)} errores/crashes detectados. Vea la tabla para detalles.")
        else:
            messagebox.showinfo("Análisis completado", "No se encontraron errores del sistema.")


def main_menu():
    root = tk.Tk()
    root.iconbitmap(resource_path("img/icon.ico"))
    root.title("Logcat Analyzer - Menú Principal")
    root.geometry("400x350")
    root.configure(bg='white')

    # Frame principal
    main_frame = tk.Frame(root, bg='white')
    main_frame.pack(expand=True, fill='both')

    # Frame para centrar botones
    center_frame = tk.Frame(main_frame, bg='white')
    center_frame.place(relx=0.5, rely=0.5, anchor='center')

    # Botón de analizar logs (VERDE)
    analyze_btn = RoundedButton(
        center_frame,
        text="Analizar logs",
        color="#90EE90",
        text_color="#006400",
        hover_color="#A2FFA2",
        corner_radius=25,
        command=analyze_log_file,
        icon_path=resource_path("img/subirArchivo.png"),
        icon_size=(20, 20),
        width=220,
        height=50
    )

    analyze_btn.pack(pady=20)

    # Botón de cerrar (ROJO)
    close_btn = RoundedButton(
        center_frame,
        text="Cerrar",
        color="#ff4444",
        text_color="white",
        hover_color="#ff6666",
        corner_radius=25,
        command=root.quit,
        icon_path=resource_path("img/close.png"),
        icon_size=(16, 16),
        font=("Arial", 10),
        width=180,
        height=40
    )

    close_btn.pack(pady=10)

    # Centrar ventana en pantalla
    root.eval('tk::PlaceWindow . center')

    root.mainloop()


if __name__ == "__main__":
    main_menu()