import 'dart:async';

enum LoginErrorType { invalidPassword, authenticationFailed, userNotFound, unexpected }

class LoginError implements Exception {
  final LoginErrorType type;
  final String message;

  LoginError(this.type, this.message);
}

abstract class LoginUseCase {
  Future<User> execute(Credentials credentials);
}

class LoginUseCaseImpl implements LoginUseCase {
  final AuthSession authSession;
  final UserRepository userRepository;
  final PasswordValidator passwordValidator;

  LoginUseCaseImpl(this.authSession, this.userRepository, this.passwordValidator);

  @override
  Future<User> execute(Credentials credentials) async {
    try {
      if (!passwordValidator.validate(credentials.password)) {
        throw LoginError(LoginErrorType.invalidPassword, "Password does not meet the required criteria");
      }

      final token = await performLogin(credentials);
      final user = await fetchUser(token);

      return user;
    } on LoginError {
      rethrow;
    } catch (e) {
      throw LoginError(LoginErrorType.unexpected, e.toString());
    }
  }

  Future<String> performLogin(Credentials credentials) async {
    try {
      return await authSession.login(credentials);
    } catch (e) {
      throw LoginError(LoginErrorType.authenticationFailed, e.toString());
    }
  }

  Future<User> fetchUser(String token) async {
    try {
      return await userRepository.getUser(token);
    } catch (e) {
      throw LoginError(LoginErrorType.userNotFound, e.toString());
    }
  }
}