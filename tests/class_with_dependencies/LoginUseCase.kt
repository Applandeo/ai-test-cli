import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

interface LoginUseCase {
    suspend operator fun invoke(credentials: Credentials): Result<User>
}

class LoginUseCaseImpl(
    private val authSession: AuthSession,
    private val userRepository: UserRepository,
    private val passwordValidator: PasswordValidator,
    private val dispatcher: CoroutineDispatcher
) : LoginUseCase {

    override suspend operator fun invoke(credentials: Credentials): Result<User> = withContext(dispatcher) {
        try {
            if (!passwordValidator.validate(credentials.password)) {
                throw InvalidPasswordException("Password does not meet the required criteria")
            }

            val token = when (val loginResult = authSession.login(credentials)) {
                is Result.Success -> loginResult.data
                is Result.Error -> throw AuthenticationException("Login failed: ${loginResult.exception.message}")
            }

            val user = when (val userResult = userRepository.getUserById(token)) {
                is Result.Success -> userResult.data
                is Result.Error -> throw UserNotFoundException("User not found: ${userResult.exception.message}")
            }

            Result.Success(user)
        } catch (e: Exception) {
            Result.Error(e)
        }
    }
}

class UserNotFoundException(message: String) : Exception(message)