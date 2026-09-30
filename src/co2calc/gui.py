import tkinter as tk
from tkinter import ttk, messagebox

from co2calc.models import Deslocamento, MeioTransporte
from co2calc.core import gerar_resultado
from co2calc.errors import EntradaInvalidaError

TRANSPORTES_LABELS = {
    "Carro a gasolina": MeioTransporte.CARRO_GASOLINA,
    "Moto": MeioTransporte.MOTO,
    "Ônibus": MeioTransporte.ONIBUS,
    "Metrô": MeioTransporte.METRO,
    "Bicicleta/Caminhada": MeioTransporte.BICICLETA_CAMINHADA,
}

CORES = {
    "fundo": "#f4f8f4",
    "primaria": "#2e7d32",
    "primaria_escura": "#1b5e20",
    "texto": "#1a1a1a",
    "card": "#ffffff",
}


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora de Emissão de CO2")
        self.geometry("420x520")
        self.resizable(False, False)
        self.configure(bg=CORES["fundo"])
        self._montar_estilo()
        self._montar_layout()

    def _montar_estilo(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "TLabel",
            background=CORES["fundo"],
            foreground=CORES["texto"],
            font=("Segoe UI", 10),
        )
        style.configure(
            "Titulo.TLabel",
            font=("Segoe UI", 16, "bold"),
            foreground=CORES["primaria_escura"],
        )
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=8)

    def _montar_layout(self):
        container = tk.Frame(self, bg=CORES["fundo"], padx=24, pady=24)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="🌳 EcoTracer", style="Titulo.TLabel").pack(
            pady=(0, 4)
        )
        ttk.Label(
            container, text="ODS 13 — Ação Contra a Mudança Global do Clima"
        ).pack(pady=(0, 16))

        ttk.Label(container, text="Distância diária (km)").pack(anchor="w")
        self.entrada_distancia = ttk.Entry(container)
        self.entrada_distancia.pack(fill="x", pady=(0, 12))

        ttk.Label(container, text="Meio de transporte").pack(anchor="w")
        self.combo_transporte = ttk.Combobox(
            container, values=list(TRANSPORTES_LABELS.keys()), state="readonly"
        )
        self.combo_transporte.current(0)
        self.combo_transporte.pack(fill="x", pady=(0, 12))

        ttk.Label(container, text="Dias por semana (1 a 7)").pack(anchor="w")
        self.entrada_dias = ttk.Entry(container)
        self.entrada_dias.pack(fill="x", pady=(0, 20))

        ttk.Button(container, text="Calcular", command=self.calcular).pack(
            fill="x", pady=(0, 20)
        )

        self.card_resultado = tk.Frame(
            container,
            bg=CORES["card"],
            padx=16,
            pady=16,
            highlightbackground=CORES["primaria"],
            highlightthickness=1,
        )
        self.card_resultado.pack(fill="both", expand=True)

        self.label_resultado = tk.Label(
            self.card_resultado,
            text="Preencha os dados e clique em Calcular.",
            bg=CORES["card"],
            fg=CORES["texto"],
            font=("Segoe UI", 10),
            justify="left",
            wraplength=340,
        )
        self.label_resultado.pack(anchor="w")

    def _ler_formulario(self) -> Deslocamento:
        distancia = float(self.entrada_distancia.get().replace(",", "."))
        dias = int(self.entrada_dias.get())
        transporte = TRANSPORTES_LABELS[self.combo_transporte.get()]
        return Deslocamento(
            distancia_km=distancia, transporte=transporte, dias_por_semana=dias
        )

    def calcular(self):
        try:
            deslocamento = self._ler_formulario()
            resultado = gerar_resultado(deslocamento)
            texto = (
                f"Emissão diária: {resultado.emissao_diaria_kg} kg de CO₂\n"
                f"Emissão anual: {resultado.emissao_anual_kg} kg de CO₂\n"
                f"Equivalente a {resultado.arvores_equivalentes} árvores/ano para compensar"
            )
            self.label_resultado.config(text=texto, fg=CORES["primaria_escura"])
        except ValueError:
            messagebox.showerror(
                "Erro", "Digite números válidos para distância e dias."
            )
        except EntradaInvalidaError as e:
            messagebox.showerror("Erro nos dados", str(e))
        except Exception as e:
            messagebox.showerror("Erro inesperado", str(e))


def executar():
    app = App()
    app.mainloop()
