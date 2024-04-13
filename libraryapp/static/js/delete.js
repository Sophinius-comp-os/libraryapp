let bookIdToDelete = null;
function confirmDelete(bookId) {
    bookIdToDelete = bookId;
    $('#deleteConfirmationModal').modal('show');
}
function proceedToDelete() {
    if (bookIdToDelete) {
        $(`#deleteForm${bookIdToDelete}`).submit();
    }
}
