class PasswordValidator {
    private let minLength: Int
    private let maxLength: Int
    private let requireUppercase: Bool
    private let requireLowercase: Bool
    private let requireDigit: Bool
    private let requireSpecialChar: Bool
    private let forbiddenChars: Set<Character>

    private init(builder: Builder) {
        self.minLength = builder.minLength
        self.maxLength = builder.maxLength
        self.requireUppercase = builder.requireUppercase
        self.requireLowercase = builder.requireLowercase
        self.requireDigit = builder.requireDigit
        self.requireSpecialChar = builder.requireSpecialChar
        self.forbiddenChars = builder.forbiddenChars
    }

    enum ValidationResult {
        case valid
        case invalid([String])
    }

    func validate(_ password: String) -> ValidationResult {
        var errors = [String]()

        if password.count < minLength { errors.append("Password is too short") }
        if password.count > maxLength { errors.append("Password is too long") }
        if requireUppercase && !password.contains(where: { $0.isUppercase }) { errors.append("Missing uppercase letter") }
        if requireLowercase && !password.contains(where: { $0.isLowercase }) { errors.append("Missing lowercase letter") }
        if requireDigit && !password.contains(where: { $0.isNumber }) { errors.append("Missing digit") }
        if requireSpecialChar && !password.contains(where: { !$0.isLetter && !$0.isNumber }) { errors.append("Missing special character") }
        if password.contains(where: { forbiddenChars.contains($0) }) { errors.append("Contains forbidden character") }

        return errors.isEmpty ? .valid : .invalid(errors)
    }

    class Builder {
        var minLength: Int = 8
        var maxLength: Int = 64
        var requireUppercase: Bool = false
        var requireLowercase: Bool = false
        var requireDigit: Bool = false
        var requireSpecialChar: Bool = false
        var forbiddenChars: Set<Character> = []

        func setMinLength(_ length: Int) -> Builder {
            self.minLength = length
            return self
        }

        func setMaxLength(_ length: Int) -> Builder {
            self.maxLength = length
            return self
        }

        func setRequireUppercase(_ require: Bool) -> Builder {
            self.requireUppercase = require
            return self
        }

        func setRequireLowercase(_ require: Bool) -> Builder {
            self.requireLowercase = require
            return self
        }

        func setRequireDigit(_ require: Bool) -> Builder {
            self.requireDigit = require
            return self
        }

        func setRequireSpecialChar(_ require: Bool) -> Builder {
            self.requireSpecialChar = require
            return self
        }

        func setForbiddenChars(_ chars: Set<Character>) -> Builder {
            self.forbiddenChars = chars
            return self
        }

        func build() throws -> PasswordValidator {
            guard minLength > 0 else {
                throw ValidationError.invalidMinLength
            }
            guard maxLength >= minLength else {
                throw ValidationError.invalidMaxLength
            }
            return PasswordValidator(builder: self)
        }

        enum ValidationError: Error {
            case invalidMinLength
            case invalidMaxLength
        }
    }

    static func build(_ configuration: (Builder) -> Void) throws -> PasswordValidator {
        let builder = Builder()
        configuration(builder)
        return try builder.build()
    }
}