extension Int {
    /**
     Divides this non-negative integer by a positive integer, returning a double precision result.

     This function performs floating-point division, where `self` is the numerator
     and the `denominator` is the divisor. Both the numerator (`self`) and
     the denominator must satisfy specific conditions for the operation to be valid.

     - Parameter denominator: The positive integer to divide by.
     - Returns: The result of the division as a `Double`.
     - Precondition: `self` must be non-negative and `denominator` must be positive.

     # Example
     ```
     let result1 = 10.divideByPositive(3)  // Returns 3.3333333333333335
     let result2 = 3.divideByPositive(2)   // Returns 1.5
     ```

     - Note: This function returns a `Double` to preserve the precision of the division result.
     - SeeAlso: The standard division operator `/` for integer division.
     */
    func divideByPositive(_ denominator: Int) -> Double {
        precondition(self >= 0, "Numerator must be non-negative, but was \(self)")
        precondition(denominator > 0, "Denominator must be positive, but was \(denominator)")

        return Double(self) / Double(denominator)
    }
}