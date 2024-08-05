import $api from "@/http";

export default class AuthService {
    static async login(username, password) {
        return $api.post("/users/login", {username, password})
    }

    static async register(username, password) {
        return $api.post("/users/register", {username, password})
    }

    static async logout() {
        return $api.post("/users/auth/logout", {})
    }

    static async refreshToken() {
        return $api.get("/users/auth/refresh");
    }
}
