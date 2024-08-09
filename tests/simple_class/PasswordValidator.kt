class PasswordValidator private constructor(builder: Builder) {
    private val minLength: Int
    private val maxLength: Int
    private val requireUppercase: Boolean
    private val requireLowercase: Boolean
    private val requireDigit: Boolean
    private val requireSpecialChar: Boolean
    private val forbiddenChars: Set<Char>

    init {
        with(builder) {
            minLength = this.minLength
            maxLength = this.maxLength
            requireUppercase = this.requireUppercase
            requireLowercase = this.requireLowercase
            requireDigit = this.requireDigit
            requireSpecialChar = this.requireSpecialChar
            forbiddenChars = this.forbiddenChars
        }
    }

    fun validate(password: String): ValidationResult {
        val errors = mutableListOf<String>()

        if (password.length < minLength) errors.add("Password is too short")
        if (password.length > maxLength) errors.add("Password is too long")
        if (requireUppercase && !password.any { it.isUpperCase() }) errors.add("Missing uppercase letter")
        if (requireLowercase && !password.any { it.isLowerCase() }) errors.add("Missing lowercase letter")
        if (requireDigit && !password.any { it.isDigit() }) errors.add("Missing digit")
        if (requireSpecialChar && !password.any { !it.isLetterOrDigit() }) errors.add("Missing special character")
        if (password.any { it in forbiddenChars }) errors.add("Contains forbidden character")

        return if (errors.isEmpty()) ValidationResult.Valid else ValidationResult.Invalid(errors)
    }

    sealed class ValidationResult {
        object Valid : ValidationResult()
        data class Invalid(val errors: List<String>) : ValidationResult()
    }

    class Builder {
        var minLength: Int = 8
        var maxLength: Int = 64
        var requireUppercase: Boolean = false
        var requireLowercase: Boolean = false
        var requireDigit: Boolean = false
        var requireSpecialChar: Boolean = false
        var forbiddenChars: Set<Char> = emptySet()

        fun minLength(length: Int) = apply { this.minLength = length }
        fun maxLength(length: Int) = apply { this.maxLength = length }
        fun requireUppercase(require: Boolean) = apply { this.requireUppercase = require }
        fun requireLowercase(require: Boolean) = apply { this.requireLowercase = require }
        fun requireDigit(require: Boolean) = apply { this.requireDigit = require }
        fun requireSpecialChar(require: Boolean) = apply { this.requireSpecialChar = require }
        fun forbidChars(chars: Set<Char>) = apply { this.forbiddenChars = chars }

        fun build(): PasswordValidator {
            require(minLength > 0) { "Minimum length must be positive" }
            require(maxLength >= minLength) { "Maximum length must be greater than or equal to minimum length" }
            return PasswordValidator(this)
        }
    }

    companion object {
        inline fun build(block: Builder.() -> Unit) = Builder().apply(block).build()
    }
}