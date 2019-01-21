class Estadisticas:
    def __init__(self, casino):
        self.casino = casino

    def resultados(self):
        msg0 = '\n#### ESTADÍSTICAS SIMULACIÓN ####'
        msg12 = self._estadisticas_ganancias_por_clientes()
        msg34 = self._estadisticas_tiempo_por_clientes()
        msg56 = self._estadisticas_ganancias()
        msg7 = self._estadisticas_trampa_ruleta()
        msg8 = self._estadisticas_salida()
        msg9 = self._estadisticas_tiempo_sin_funcionar()
        msg10 = self._estadisticas_cantidad_clientes()
        e = '\n'
        resultado = (msg0 + e + msg12 + e + msg34 + e + msg56 + e + msg7 + e
                     + msg8 + e + msg9 + e + msg10)
        self._guardar_resultados(resultado)
        return resultado

    def _guardar_resultados(self, resultado):
        with open('resultados_simulacion.txt', 'w', encoding='utf8') as file:
            file.write(resultado)

    def _suma_diccionario(selfl, diccionario):
        valor = {p: sum(n) for p, n in diccionario.items()}
        total = sum(n for n in valor.values())
        return total, valor

    def _estadisticas_ganancias_por_clientes(self):
        c_total, c_personalidad = self._suma_diccionario(
            self.casino.personalidad_clientes)
        g_total, g_personalidad = self._suma_diccionario(
            self.casino.ganancias_personalidad)
        g_promedio = g_total / max(c_total, 1)
        g_promedio_pers = {p: g / max(1, c_personalidad[p])
                           for p, g in g_personalidad.items()}

        msg1 = f'1.- Ganancias promedio por cliente: {round(g_promedio, 3)}\n'
        msg2 = f'2.- Ganancias promedio por personalidad:\n'
        msg3 = [f'    {p}: {round(g ,3)}' for p, g in g_promedio_pers.items()]
        return msg1 + msg2 + '\n'.join(msg3)

    def _estadisticas_tiempo_por_clientes(self):
        c_total, c_personalidad = self._suma_diccionario(
            self.casino.personalidad_clientes)
        t_total, t_personalidad = self._suma_diccionario(
            self.casino.tiempo_estadia)
        t_promedio = round(t_total / max(c_total, 1),2)
        t_promedio_p = {p: t / max(1, c_personalidad[p])
                           for p, t in t_personalidad.items()}

        msg1 = f'3.- Tiempo promedio estadía por cliente: {t_promedio} min\n'
        msg2 = f'4.- Tiempo promedio estadía por personalidad:\n'
        msg3 = [f'    {p}: {round(t, 2)} min' for p, t in t_promedio_p.items()]
        return msg1 + msg2 + '\n'.join(msg3)

    def _estadisticas_ganancias(self):
        g_restobar = self.casino.restobar.ganancias
        g_tarot = self.casino.tarot.ganancias
        g_bano = self.casino.bano.ganancias
        g_tragamoneda = self.casino.tragamonedas.ganancias + \
                        self.casino.tragamonedas.pozo
        g_ruleta = self.casino.ruleta.ganancias
        g_tini = self.casino.tini_padrini.ganancias
        ganancias = (g_restobar + g_tarot + g_bano + g_tragamoneda + g_ruleta
                     + g_tini)
        total_dias = self.casino.tiempo / (24 * 60 * 60)
        g_diaria = ganancias / total_dias

        p_tragamoneda = self.casino.tragamonedas.ganancias * 9 - \
                        self.casino.tragamonedas.pozo
        p_ruleta = self.casino.ruleta.dinero_apostado
        msg1 = f'5.- Ganancias promedio por día: {round(g_diaria,2)}\n'

        if g_tragamoneda / p_tragamoneda > g_ruleta / p_ruleta:
            juego= f'6.- El tragamonedas generó más'
        elif g_tragamoneda / p_tragamoneda < g_ruleta / p_ruleta:
            juego = f'6.- La ruleta generó más'
        else:
            juego = f'6.- Ambos juegos generaron igual'
        msg2 = f'{juego} ganancias en comparación a los premios que entregó.'
        return msg1 + msg2

    def _estadisticas_trampa_ruleta(self):
        ''' Porcentaje de clientes que contó cartas. No necesariamente fueron
        descubiertas. '''
        total, razones = self._suma_diccionario(self.casino.razones_salida)
        total_trampa = len(self.casino.ruleta.contadores_carta)
        p_trampa = total_trampa / max(1, total)
        return f'7.- Porcentaje de personas que contó cartas: {p_trampa * 100}%'

    def _estadisticas_salida(self):
        total, razones = self._suma_diccionario(self.casino.razones_salida)
        p_razon = [f'  {r}: {round(t / total * 100,2)}%'
                   for r, t in razones.items()]
        msg1 = '8.- Razones de salida del casino:\n  '
        msg2 = '\n  '.join(p_razon)
        return msg1 + msg2

    def _estadisticas_tiempo_sin_funcionar(self):
        instalaciones = {'Restobar': self.casino.restobar,
                         'Tarot': self.casino.tarot,
                         'Baño': self.casino.bano, 'Ruleta': self.casino.ruleta,
                         'Tragamonedas': self.casino.tragamonedas}
        msg0 = '9.- Tiempo sin funcionar de cada instalación en minutos:\n'
        msgs = [f'    {n}: {inst.tiempo_cerrado}'
                for n, inst in instalaciones.items()]
        return msg0 + '\n'.join(msgs)

    def _estadisticas_cantidad_clientes(self):
        msg0 = '10.- Número de personas que visit́o cada juego ' \
               'en promedio por d́ıa:\n'
        dias = self.casino.tiempo / (24 * 60 * 60)
        msg1 = f'    Ruleta: {round(self.casino.ruleta.n_clientes / dias, 2)}\n'
        msg2 = f'    Tragamonedas: ' \
               f'{round(self.casino.tragamonedas.n_clientes / dias, 2)}'
        return msg0 + msg1 + msg2

