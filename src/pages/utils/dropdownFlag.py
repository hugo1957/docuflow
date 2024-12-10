import flet as ft

class CountryDropdown(ft.UserControl):
    def __init__(self, on_country_change=None):
        super().__init__()
        self.on_country_change = on_country_change
        
        self.country_data = {
    "Afghanistan": {"flag": "flags/af.png"},
    "Albania": {"flag": "flags/al.png"},
    "Algeria": {"flag": "flags/dz.png"},
    "Andorra": {"flag": "flags/ad.png"},
    "Angola": {"flag": "flags/ao.png"},
    "Antigua and Barbuda": {"flag": "flags/ag.png"},
    "Argentina": {"flag": "flags/ar.png"},
    "Armenia": {"flag": "flags/am.png"},
    "Australia": {"flag": "flags/au.png"},
    "Austria": {"flag": "flags/at.png"},
    "Azerbaijan": {"flag": "flags/az.png"},
    "Bahamas": {"flag": "flags/bs.png"},
    "Bahrain": {"flag": "flags/bh.png"},
    "Bangladesh": {"flag": "flags/bd.png"},
    "Barbados": {"flag": "flags/bb.png"},
    "Belarus": {"flag": "flags/by.png"},
    "Belgium": {"flag": "flags/be.png"},
    "Belize": {"flag": "flags/bz.png"},
    "Benin": {"flag": "flags/bj.png"},
    "Bhutan": {"flag": "flags/bt.png"},
    "Bolivia": {"flag": "flags/bo.png"},
    "Bosnia and Herzegovina": {"flag": "flags/ba.png"},
    "Botswana": {"flag": "flags/bw.png"},
    "Brazil": {"flag": "flags/br.png"},
    "Brunei": {"flag": "flags/bn.png"},
    "Bulgaria": {"flag": "flags/bg.png"},
    "Burkina Faso": {"flag": "flags/bf.png"},
    "Burundi": {"flag": "flags/bi.png"},
    "Cambodia": {"flag": "flags/kh.png"},
    "Cameroon": {"flag": "flags/cm.png"},
    "Canada": {"flag": "flags/ca.png"},
    "Cape Verde": {"flag": "flags/cv.png"},
    "Central African Republic": {"flag": "flags/cf.png"},
    "Chad": {"flag": "flags/td.png"},
    "Chile": {"flag": "flags/cl.png"},
    "China": {"flag": "flags/cn.png"},
    "Colombia": {"flag": "flags/co.png"},
    "Comoros": {"flag": "flags/km.png"},
    "Congo (Brazzaville)": {"flag": "flags/cg.png"},
    "Congo (Kinshasa)": {"flag": "flags/cd.png"},
    "Costa Rica": {"flag": "flags/cr.png"},
    "Croatia": {"flag": "flags/hr.png"},
    "Cuba": {"flag": "flags/cu.png"},
    "Cyprus": {"flag": "flags/cy.png"},
    "Czech Republic": {"flag": "flags/cz.png"},
    "Denmark": {"flag": "flags/dk.png"},
    "Djibouti": {"flag": "flags/dj.png"},
    "Dominica": {"flag": "flags/dm.png"},
    "Dominican Republic": {"flag": "flags/do.png"},
    "Ecuador": {"flag": "flags/ec.png"},
    "Egypt": {"flag": "flags/eg.png"},
    "El Salvador": {"flag": "flags/sv.png"},
    "Equatorial Guinea": {"flag": "flags/gq.png"},
    "Eritrea": {"flag": "flags/er.png"},
    "Estonia": {"flag": "flags/ee.png"},
    "Eswatini": {"flag": "flags/sz.png"},
    "Ethiopia": {"flag": "flags/et.png"},
    "Fiji": {"flag": "flags/fj.png"},
    "Finland": {"flag": "flags/fi.png"},
    "France": {"flag": "flags/fr.png"},
    "Gabon": {"flag": "flags/ga.png"},
    "Gambia": {"flag": "flags/gm.png"},
    "Georgia": {"flag": "flags/ge.png"},
    "Germany": {"flag": "flags/de.png"},
    "Ghana": {"flag": "flags/gh.png"},
    "Greece": {"flag": "flags/gr.png"},
    "Grenada": {"flag": "flags/gd.png"},
    "Guatemala": {"flag": "flags/gt.png"},
    "Guinea": {"flag": "flags/gn.png"},
    "Guinea-Bissau": {"flag": "flags/gw.png"},
    "Guyana": {"flag": "flags/gy.png"},
    "Haiti": {"flag": "flags/ht.png"},
    "Honduras": {"flag": "flags/hn.png"},
    "Hungary": {"flag": "flags/hu.png"},
    "Iceland": {"flag": "flags/is.png"},
    "India": {"flag": "flags/in.png"},
    "Indonesia": {"flag": "flags/id.png"},
    "Iran": {"flag": "flags/ir.png"},
    "Iraq": {"flag": "flags/iq.png"},
    "Ireland": {"flag": "flags/ie.png"},
    "Israel": {"flag": "flags/il.png"},
    "Italy": {"flag": "flags/it.png"},
    # Continuar con la lista...
}


        self.dropdown = None

    def handle_country_change(self, e):
        # Llama al callback de cambio de país si está definido
        if self.on_country_change:
            self.on_country_change(e.control.value)

    def build(self):
        # Opciones para el Dropdown
        dropdown_options = [
            ft.dropdown.Option(
                key=key,
                content=ft.Row(
                    [
                        ft.Image(src=value["flag"], width=20, height=20),
                        ft.Text(key, size=14, color=ft.Colors.BLACK),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
            )
            for key, value in self.country_data.items()
        ]

        # Dropdown
        self.dropdown = ft.Dropdown(
            options=dropdown_options,
            value=None,  # Selección inicial vacía
            height=70,
            border_radius=ft.border_radius.all(15),
            padding=ft.padding.all(5),
            bgcolor=ft.Colors.WHITE,
            border_width=0.5,
            on_change=self.handle_country_change,
            autofocus=False,
            filled=False,
        )

        return self.dropdown
