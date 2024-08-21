extension IntExtension on int {
  /// Divides this non-negative integer by a positive integer, returning a double precision result.
  ///
  /// [denominator]: The positive integer to divide by.
  /// Returns: The result of the division as a [double].
  /// Throws: [ArgumentError] if `this` is negative or [denominator] is not positive.
  ///
  /// Example:
  /// ```dart
  /// final result1 = 10.divideByPositive(3);  // Returns 3.3333333333333335
  /// final result2 = 3.divideByPositive(2);   // Returns 1.5
  /// ```
  ///
  double divideByPositive(int denominator) {
    if (this < 0) {
      throw ArgumentError('Numerator must be non-negative, but was $this');
    }
    if (denominator <= 0) {
      throw ArgumentError('Denominator must be positive, but was $denominator');
    }

    return this / denominator;
  }
}