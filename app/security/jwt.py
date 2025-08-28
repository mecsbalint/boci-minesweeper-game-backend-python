
def init_flask_jwt(jwt_manager):

    @jwt_manager.user_lookup_loader
    def user_lookup_callback(jwt_header, jwt_payload) -> int:
        user_id = jwt_payload["sub"]
        return user_id
