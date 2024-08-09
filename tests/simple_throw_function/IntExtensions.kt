/**
 * Divides this non-negative integer by a positive integer, returning a double precision result.
 *
 * This function performs floating-point division, where this [Int] is the numerator
 * and the [denominator] is the divisor. Both the numerator (this integer) and
 * the denominator must satisfy specific conditions for the operation to be valid.
 *
 * @param denominator The positive integer to divide by.
 * @return The result of the division as a [Double].
 * @throws IllegalArgumentException if this integer is negative or if the denominator is not positive.
 *
 * @sample
 * ```
 * val result1 = 10.divideByPositive(3)  // Returns 3.3333333333333335
 * val result2 = 3.divideByPositive(2)   // Returns 1.5
 * ```
 *
 * @see div for standard integer division.
 */
fun Int.divideByPositive(denominator: Int): Double {
    require(this >= 0) { "Numerator must be non-negative, but was $this" }
    require(denominator > 0) { "Denominator must be positive, but was $denominator" }

    return this.toDouble() / denominator.toDouble()
}