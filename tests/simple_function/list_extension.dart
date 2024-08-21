extension ListExtension<E> on List<E> {
  /// Replaces an element at the specified index with a new element.
  ///
  /// Parameters:
  ///   [index]: The index at which to replace the element.
  ///   [newElement]: The new element to be placed at the specified index.
  /// Returns: A new list with the element replaced at the specified index.
  ///
  /// This function handles three cases:
  /// 1. If the index is out of bounds, it returns the original list unchanged.
  /// 2. If the list has only one element, it returns a new list with just the new element.
  /// 3. For lists with more than one element, it creates a new list by combining:
  ///    - The slice of the original list from the start up to (but not including) the specified index
  ///    - The new element
  ///    - The slice of the original list from the index after the specified index to the end
  List<E> replacingElement(int index, E newElement) {
    if (index < 0 || index >= length) {
      return this;
    }

    if (length == 1) {
      return [newElement];
    } else {
      return [...sublist(0, index), newElement, ...sublist(index + 1)];
    }
  }
}