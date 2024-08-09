protocol LoginUseCase {
    func callAsFunction(credentials: Credentials) async -> Result<User, LoginError>
}

class LoginUseCaseImpl: LoginUseCase {
    private let authSession: AuthSession
    private let userRepository: UserRepository
    private let passwordValidator: PasswordValidator

    init(authSession: AuthSession,
         userRepository: UserRepository,
         passwordValidator: PasswordValidator) {
        self.authSession = authSession
        self.userRepository = userRepository
        self.passwordValidator = passwordValidator
    }

    func callAsFunction(credentials: Credentials) async -> Result<User, LoginError> {
        do {
            guard passwordValidator.validate(credentials.password) else {
                throw LoginError.invalidPassword("Password does not meet the required criteria")
            }

            let token = try await performLogin(credentials: credentials)
            let user = try await fetchUser(withToken: token)

            return .success(user)
        } catch let error as LoginError {
            return .failure(error)
        } catch {
            return .failure(.unexpected(error.localizedDescription))
        }
    }

    private func performLogin(credentials: Credentials) async throws -> String {
        switch await authSession.login(credentials: credentials) {
        case .success(let token):
            return token
        case .failure(let error):
            throw LoginError.authenticationFailed(error.localizedDescription)
        }
    }

    private func fetchUser(withToken token: String) async throws -> User {
        switch await userRepository.getUser(byId: token) {
        case .success(let user):
            return user
        case .failure(let error):
            throw LoginError.userNotFound(error.localizedDescription)
        }
    }
}