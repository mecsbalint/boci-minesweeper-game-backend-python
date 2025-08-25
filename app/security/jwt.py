
def init_flask_jwt(jwt_manager):

    @jwt_manager.user_lookup_loader
    def user_lookup_callback(jwt_header, jwt_payload):
        user_email = jwt_payload["sub"]
        return user_email
