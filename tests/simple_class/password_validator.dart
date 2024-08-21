import 'dart:core';

enum ValidationResult {
    valid,
    invalid,
}

class PasswordValidator {
  final int minLength;
  final int maxLength;
  final bool requireUppercase;
  final bool requireLowercase;
  final bool requireDigit;
  final bool requireSpecialChar;
  final Set<String> forbiddenChars;

  PasswordValidator._({
    required this.minLength,
    required this.maxLength,
    required this.requireUppercase,
    required this.requireLowercase,
    required this.requireDigit,
    required this.requireSpecialChar,
    required this.forbiddenChars,
  });

  ValidationResult validate(String password) {
    List<String> errors = [];

    if (password.length < minLength) errors.add("Password is too short");
    if (password.length > maxLength) errors.add("Password is too long");
    if (requireUppercase && !password.contains(RegExp(r'[A-Z]'))) errors.add("Missing uppercase letter");
    if (requireLowercase && !password.contains(RegExp(r'[a-z]'))) errors.add("Missing lowercase letter");
    if (requireDigit && !password.contains(RegExp(r'\d'))) errors.add("Missing digit");
    if (requireSpecialChar && !password.contains(RegExp(r'[!@#$%^&*(),.?":{}|<>]'))) errors.add("Missing special character");
    if (password.split('').any((char) => forbiddenChars.contains(char))) errors.add("Contains forbidden character");

    return errors.isEmpty ? ValidationResult.valid : ValidationResult.invalid;
  }

  static Builder builder() => Builder();

  static Future<PasswordValidator> build(Function(Builder) configuration) async {
    final builder = Builder();
    configuration(builder);
    return builder.build();
  }
}

class Builder {
  int minLength = 8;
  int maxLength = 64;
  bool requireUppercase = false;
  bool requireLowercase = false;
  bool requireDigit = false;
  bool requireSpecialChar = false;
  Set<String> forbiddenChars = {};

  Builder setMinLength(int length) {
    minLength = length;
    return this;
  }

  Builder setMaxLength(int length) {
    maxLength = length;
    return this;
  }

  Builder setRequireUppercase(bool require) {
    requireUppercase = require;
    return this;
  }

  Builder setRequireLowercase(bool require) {
    requireLowercase = require;
    return this;
  }

  Builder setRequireDigit(bool require) {
    requireDigit = require;
    return this;
  }

  Builder setRequireSpecialChar(bool require) {
    requireSpecialChar = require;
    return this;
  }

  Builder setForbiddenChars(Set<String> chars) {
    forbiddenChars = chars;
    return this;
  }

  Future<PasswordValidator> build() async {
    if (minLength <= 0) {
      throw ValidationError('Invalid minimum length');
    }
    if (maxLength < minLength) {
      throw ValidationError('Invalid maximum length');
    }
    return PasswordValidator._(
      minLength: minLength,
      maxLength: maxLength,
      requireUppercase: requireUppercase,
      requireLowercase: requireLowercase,
      requireDigit: requireDigit,
      requireSpecialChar: requireSpecialChar,
      forbiddenChars: forbiddenChars,
    );
  }
}

class ValidationError implements Exception {
  final String message;
  ValidationError(this.message);

  @override
  String toString() => 'ValidationError: $message';
}