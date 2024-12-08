import flet as ft


class PhoneInputDropdown(ft.UserControl):
    def __init__(self, on_country_change=None, on_phone_change=None):
        super().__init__()
        self.on_country_change = on_country_change
        self.on_phone_change = on_phone_change

        self.country_data = {
            "+93": {"flag": "flags/af.png", "length": 9},
            "+355": {"flag": "flags/al.png", "length": 9},
            "+213": {"flag": "flags/dz.png", "length": 9},
            "+376": {"flag": "flags/ad.png", "length": 6},
            "+244": {"flag": "flags/ao.png", "length": 9},
            "+54": {"flag": "flags/ar.png", "length": 13},
            "+374": {"flag": "flags/am.png", "length": 8},
            "+297": {"flag": "flags/aw.png", "length": 7},
            "+61": {"flag": "flags/au.png", "length": 9},
            "+43": {"flag": "flags/at.png", "length": 10},
            "+994": {"flag": "flags/az.png", "length": 9},
            "+973": {"flag": "flags/bh.png", "length": 8},
            "+880": {"flag": "flags/bd.png", "length": 10},
            "+375": {"flag": "flags/by.png", "length": 9},
            "+32": {"flag": "flags/be.png", "length": 9},
            "+501": {"flag": "flags/bz.png", "length": 7},
            "+229": {"flag": "flags/bj.png", "length": 8},
            "+975": {"flag": "flags/bt.png", "length": 8},
            "+591": {"flag": "flags/bo.png", "length": 8},
            "+387": {"flag": "flags/ba.png", "length": 8},
            "+267": {"flag": "flags/bw.png", "length": 7},
            "+55": {"flag": "flags/br.png", "length": 11},
            "+673": {"flag": "flags/bn.png", "length": 7},
            "+359": {"flag": "flags/bg.png", "length": 9},
            "+226": {"flag": "flags/bf.png", "length": 8},
            "+257": {"flag": "flags/bi.png", "length": 8},
            "+238": {"flag": "flags/cv.png", "length": 7},
            "+855": {"flag": "flags/kh.png", "length": 9},
            "+237": {"flag": "flags/cm.png", "length": 9},
            "+1": {"flag": "flags/ca.png", "length": 10},
            "+235": {"flag": "flags/td.png", "length": 8},
            "+56": {"flag": "flags/cl.png", "length": 9},
            "+86": {"flag": "flags/cn.png", "length": 11},
            "+57": {"flag": "flags/co.png", "length": 10},
            "+269": {"flag": "flags/km.png", "length": 7},
            "+242": {"flag": "flags/cg.png", "length": 9},
            "+243": {"flag": "flags/cd.png", "length": 9},
            "+682": {"flag": "flags/ck.png", "length": 5},
            "+506": {"flag": "flags/cr.png", "length": 8},
            "+225": {"flag": "flags/ci.png", "length": 8},
            "+385": {"flag": "flags/hr.png", "length": 9},
            "+53": {"flag": "flags/cu.png", "length": 8},
            "+357": {"flag": "flags/cy.png", "length": 8},
            "+420": {"flag": "flags/cz.png", "length": 9},
            "+45": {"flag": "flags/dk.png", "length": 8},
            "+253": {"flag": "flags/dj.png", "length": 8},
            "+593": {"flag": "flags/ec.png", "length": 10},
            "+20": {"flag": "flags/eg.png", "length": 10},
            "+503": {"flag": "flags/sv.png", "length": 8},
            "+240": {"flag": "flags/gq.png", "length": 9},
            "+291": {"flag": "flags/er.png", "length": 7},
            "+372": {"flag": "flags/ee.png", "length": 8},
            "+251": {"flag": "flags/et.png", "length": 9},
            "+679": {"flag": "flags/fj.png", "length": 7},
            "+358": {"flag": "flags/fi.png", "length": 10},
            "+33": {"flag": "flags/fr.png", "length": 9},
            "+241": {"flag": "flags/ga.png", "length": 9},
            "+220": {"flag": "flags/gm.png", "length": 7},
            "+995": {"flag": "flags/ge.png", "length": 9},
            "+49": {"flag": "flags/de.png", "length": 10},
            "+233": {"flag": "flags/gh.png", "length": 9},
            "+30": {"flag": "flags/gr.png", "length": 10},
            "+502": {"flag": "flags/gt.png", "length": 8},
            "+224": {"flag": "flags/gn.png", "length": 9},
            "+245": {"flag": "flags/gw.png", "length": 9},
            "+592": {"flag": "flags/gy.png", "length": 7},
            "+509": {"flag": "flags/ht.png", "length": 8},
            "+504": {"flag": "flags/hn.png", "length": 8},
            "+36": {"flag": "flags/hu.png", "length": 9},
            "+91": {"flag": "flags/in.png", "length": 10},
            "+62": {"flag": "flags/id.png", "length": 11},
            "+98": {"flag": "flags/ir.png", "length": 10},
            "+964": {"flag": "flags/iq.png", "length": 10},
            "+353": {"flag": "flags/ie.png", "length": 9},
            "+972": {"flag": "flags/il.png", "length": 9},
            "+39": {"flag": "flags/it.png", "length": 10},
            "+876": {"flag": "flags/jm.png", "length": 7},
            "+81": {"flag": "flags/jp.png", "length": 10},
            "+962": {"flag": "flags/jo.png", "length": 9},
            "+7": {"flag": "flags/kz.png", "length": 10},
            "+254": {"flag": "flags/ke.png", "length": 10},
            "+965": {"flag": "flags/kw.png", "length": 8},
            "+996": {"flag": "flags/kg.png", "length": 9},
            "+856": {"flag": "flags/la.png", "length": 9},
            "+371": {"flag": "flags/lv.png", "length": 8},
            "+961": {"flag": "flags/lb.png", "length": 8},
            "+266": {"flag": "flags/ls.png", "length": 8},
            "+231": {"flag": "flags/lr.png", "length": 8},
            "+218": {"flag": "flags/ly.png", "length": 10},
            "+423": {"flag": "flags/li.png", "length": 7},
            "+370": {"flag": "flags/lt.png", "length": 8},
            "+352": {"flag": "flags/lu.png", "length": 9},
            "+853": {"flag": "flags/mo.png", "length": 8},
            "+261": {"flag": "flags/mg.png", "length": 9},
            "+265": {"flag": "flags/mw.png", "length": 7},
            "+60": {"flag": "flags/my.png", "length": 10},
            "+960": {"flag": "flags/mv.png", "length": 7},
            "+223": {"flag": "flags/ml.png", "length": 8},
            "+356": {"flag": "flags/mt.png", "length": 8},
            "+692": {"flag": "flags/mh.png", "length": 7},
            "+596": {"flag": "flags/mq.png", "length": 9},
            "+222": {"flag": "flags/mr.png", "length": 9},
            "+230": {"flag": "flags/mu.png", "length": 8},
            "+262": {"flag": "flags/re.png", "length": 9},
            "+52": {"flag": "flags/mx.png", "length": 10},
            "+373": {"flag": "flags/md.png", "length": 8},
            "+212": {"flag": "flags/ma.png", "length": 9},
            "+258": {"flag": "flags/mz.png", "length": 9},
            "+95": {"flag": "flags/mm.png", "length": 9},
            "+264": {"flag": "flags/na.png", "length": 8},
            "+674": {"flag": "flags/nr.png", "length": 7},
            "+977": {"flag": "flags/np.png", "length": 10},
            "+31": {"flag": "flags/nl.png", "length": 9},
            "+687": {"flag": "flags/nc.png", "length": 6},
            "+64": {"flag": "flags/nz.png", "length": 9},
            "+505": {"flag": "flags/ni.png", "length": 8},
            "+227": {"flag": "flags/ne.png", "length": 8},
            "+234": {"flag": "flags/ng.png", "length": 10},
            "+47": {"flag": "flags/no.png", "length": 8},
            "+968": {"flag": "flags/om.png", "length": 8},
            "+92": {"flag": "flags/pk.png", "length": 10},
            "+680": {"flag": "flags/pw.png", "length": 7},
            "+507": {"flag": "flags/pa.png", "length": 8},
            "+595": {"flag": "flags/py.png", "length": 9},
            "+51": {"flag": "flags/pe.png", "length": 9},
            "+63": {"flag": "flags/ph.png", "length": 10},
            "+48": {"flag": "flags/pl.png", "length": 9},
            "+351": {"flag": "flags/pt.png", "length": 9},
            "+974": {"flag": "flags/qa.png", "length": 8},
            "+40": {"flag": "flags/ro.png", "length": 10},
            "+7": {"flag": "flags/ru.png", "length": 10},
            "+250": {"flag": "flags/rw.png", "length": 9},
            "+685": {"flag": "flags/ws.png", "length": 7},
            "+966": {"flag": "flags/sa.png", "length": 9},
            "+221": {"flag": "flags/sn.png", "length": 9},
            "+381": {"flag": "flags/rs.png", "length": 9},
            "+248": {"flag": "flags/sc.png", "length": 7},
            "+232": {"flag": "flags/sl.png", "length": 8},
            "+65": {"flag": "flags/sg.png", "length": 8},
            "+421": {"flag": "flags/sk.png", "length": 9},
            "+386": {"flag": "flags/si.png", "length": 9},
            "+677": {"flag": "flags/sb.png", "length": 7},
            "+252": {"flag": "flags/so.png", "length": 8},
            "+27": {"flag": "flags/za.png", "length": 9},
            "+82": {"flag": "flags/kr.png", "length": 11},
            "+211": {"flag": "flags/ss.png", "length": 9},
            "+34": {"flag": "flags/es.png", "length": 9},
            "+94": {"flag": "flags/lk.png", "length": 9},
            "+249": {"flag": "flags/sd.png", "length": 9},
            "+597": {"flag": "flags/sr.png", "length": 7},
            "+268": {"flag": "flags/sz.png", "length": 8},
            "+46": {"flag": "flags/se.png", "length": 10},
            "+41": {"flag": "flags/ch.png", "length": 9},
            "+963": {"flag": "flags/sy.png", "length": 9},
            "+886": {"flag": "flags/tw.png", "length": 9},
            "+992": {"flag": "flags/tj.png", "length": 9},
            "+255": {"flag": "flags/tz.png", "length": 9},
            "+66": {"flag": "flags/th.png", "length": 9},
            "+670": {"flag": "flags/tl.png", "length": 7},
            "+228": {"flag": "flags/tg.png", "length": 8},
            "+676": {"flag": "flags/to.png", "length": 7},
            "+216": {"flag": "flags/tn.png", "length": 8},
            "+90": {"flag": "flags/tr.png", "length": 10},
            "+993": {"flag": "flags/tm.png", "length": 8},
            "+688": {"flag": "flags/tv.png", "length": 7},
            "+256": {"flag": "flags/ug.png", "length": 9},
            "+380": {"flag": "flags/ua.png", "length": 9},
            "+971": {"flag": "flags/ae.png", "length": 9},
            "+44": {"flag": "flags/gb.png", "length": 10},
            "+598": {"flag": "flags/uy.png", "length": 9},
            "+998": {"flag": "flags/uz.png", "length": 9},
            "+678": {"flag": "flags/vu.png", "length": 7},
            "+58": {"flag": "flags/ve.png", "length": 11},
            "+84": {"flag": "flags/vn.png", "length": 9},
            "+967": {"flag": "flags/ye.png", "length": 9},
            "+260": {"flag": "flags/zm.png", "length": 9},
            "+263": {"flag": "flags/zw.png", "length": 9},
        }


        self.selected_country = "+57"  # País inicial
        self.phone_field = None
        self.dropdown = None

    def handle_country_change(self, e):
        # Actualiza la longitud máxima del TextField basado en el país seleccionado
        selected_country = self.dropdown.value
        max_length = self.country_data[selected_country]["length"]
        self.phone_field.max_length = max_length
        self.update()

    def handle_submit(self, e):
        # Validación del número de teléfono
        phone_number = self.phone_field.value
        selected_country = self.dropdown.value

        if not phone_number.isdigit():
            self.page.snack_bar = ft.SnackBar(
                ft.Text("El número de teléfono solo puede contener dígitos."),
                bgcolor=ft.Colors.RED_500,
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        if len(phone_number) < self.phone_field.max_length:
            self.page.snack_bar = ft.SnackBar(
                ft.Text("Debes ingresar un número de teléfono válido!"),
                bgcolor=ft.Colors.RED_500,
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        # Llama al callback si la validación es exitosa
        self.on_submit(selected_country, phone_number)

    def build(self):
        # Opciones para el Dropdown
        dropdown_options = [
            ft.dropdown.Option(
                key=key,
                content=ft.Row(
                    [
                        ft.Image(src=value["flag"], width=20, height=20),
                        ft.Text(f"({key})", size=12, color=ft.Colors.BLACK),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
            )
            for key, value in self.country_data.items()
        ]

        # Dropdown
        self.dropdown = ft.Dropdown(
            options=dropdown_options,
            value=self.selected_country,
            width=110,
            height=60,
            border_radius=ft.border_radius.all(15),
            padding=ft.padding.all(5),
            bgcolor=ft.Colors.WHITE,
            border_width=0.5,
            on_change=self.handle_country_change,
            autofocus=False,
            filled=False,
        )

        # TextField
        self.phone_field = ft.TextField(
            max_length=self.country_data[self.selected_country]["length"],
            width=250,
            height=60,
            border_radius=ft.border_radius.all(15),
            content_padding=ft.padding.symmetric(horizontal=20, vertical=15),
            bgcolor=ft.Colors.WHITE,
            border_color="#717171",
            label_style=ft.TextStyle(color="#717171", font_family="Poppins"),
            border_width=0.5,
            expand=True,
            filled=False,
        )

        return ft.Row(
            controls=[self.dropdown, self.phone_field],
            spacing=10,
        )
