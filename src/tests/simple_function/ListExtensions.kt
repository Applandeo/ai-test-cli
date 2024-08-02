/**
 * Replaces an item at the specified index in the list with a new item.
 *
 * @param T The type of elements in the list.
 * @param index The index at which to replace the item.
 * @param item The new item to be placed at the specified index.
 * @return A new list with the item replaced at the specified index.
 *
 * This function handles three cases:
 * 1. If the index is out of bounds, it returns the original list unchanged.
 * 2. If the list has only one element, it returns a new list with just the new item.
 * 3. For lists with more than one element, it creates a new list by combining:
 *    - The slice of the original list from the start up to (but not including) the specified index
 *    - The new item
 *    - The slice of the original list from the index after the specified index to the end
 */
fun <T> List<T>.replaceAt(index: Int, item: T): List<T> = when {
    index !in indices -> this
    size == 1 -> listOf(item)
    else -> slice(0 until index) + item + slice(index + 1 until size)
}