from flet_core.control import Control

class GoogleSignIn(Control):
    def __init__(self, client_id: str):
        super().__init__()
        self.client_id = client_id

    def _get_control_name(self):
        return "google_signin"

    def _before_build_command(self):
        self._set_attr("clientId", self.client_id)

    def sign_in(self):
        """
        Llama al método 'signIn' definido en el control Dart.
        """
        self.invoke_method("signIn")

    def on_sign_in_success(self, handler):
        """
        Registra un manejador de eventos para el éxito del inicio de sesión.
        """
        self._add_event_handler("onSignInSuccess", handler)

    def on_sign_in_error(self, handler):
        """
        Registra un manejador de eventos para los errores de inicio de sesión.
        """
        self._add_event_handler("onSignInError", handler)
