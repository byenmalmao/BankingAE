function LoginForm() {
    return (
        <div className="bg-white p-8 rounded-lg shadow-lg w-96 transform transition-all hover:shadow-xl">
            <div className="flex justify-center mb-6">
                <img src="/images/logo.png" alt="Scotia Bank Logo" className="w-32" />
            </div>
            <h2 className="text-2xl font-bold text-center text-gray-800 mb-6">Iniciar Sesión</h2>
            <form className="space-y-4">
                <div>
                    <label className="block text-gray-700 text-sm font-medium mb-1">Usuario</label>
                    <input
                        type="text"
                        name="username"
                        required
                        className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                </div>
                <div>
                    <label className="block text-gray-700 text-sm font-medium mb-1">Contraseña</label>
                    <input
                        type="password"
                        name="password"
                        required
                        className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                </div>
                <button
                    type="submit"
                    className="w-full bg-blue-600 text-white p-2 rounded-lg hover:bg-blue-700 transition duration-300"
                >
                    Ingresar
                </button>
            </form>
        </div>
    );
}

export default LoginForm;