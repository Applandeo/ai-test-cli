extension Array {
    /// Replaces an element at the specified index with a new element.
    ///
    /// - Parameters:
    ///   - index: The index at which to replace the element.
    ///   - newElement: The new element to be placed at the specified index.
    /// - Returns: A new array with the element replaced at the specified index.
    ///
    /// This function handles three cases:
    /// 1. If the index is out of bounds, it returns the original array unchanged.
    /// 2. If the array has only one element, it returns a new array with just the new element.
    /// 3. For arrays with more than one element, it creates a new array by combining:
    ///    - The slice of the original array from the start up to (but not including) the specified index
    ///    - The new element
    ///    - The slice of the original array from the index after the specified index to the end
    func replacingElement(at index: Int, with newElement: Element) -> [Element] {
        guard index >= 0 && index < count else { return self }

        if count == 1 {
            return [newElement]
        } else {
            var newArray = self
            newArray[index] = newElement
            return newArray
        }
    }
}