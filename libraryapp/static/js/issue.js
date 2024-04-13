$(document).ready(function () {
    // On page load, fetch the list of books and members with negative balance
    $.ajax({
        url: '/get_all/',
        method: 'GET',
        success: function (data) {
            var bookDropdown = $('#book');
            bookDropdown.empty().append($('<option>', {
                value: '',
                text: 'Select a book'
            }));
            $.each(data.books, function (index, book) {
                bookDropdown.append($('<option>', {
                    value: book.id,
                    text: book.title 
                }));
            });

            var memberDropdown = $('#member');
            memberDropdown.empty().append($('<option>', {
                value: '',
                text: 'Select a member'
            }));
            $.each(data.members, function (index, member) {
                memberDropdown.append($('<option>', {
                    value: member.id,
                    text: member.name
                }));
            });
        },
        error: function (error) {
            console.error('Error fetching data:', error);
        }
    });
    $('#book').change(function () {
        var selectedBookId = $(this).val();
        console.log('Selected Book ID:', selectedBookId);
    });
    
});
function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = $.trim(cookies[i]);
                // Check if this cookie string begins with the name we want
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    // Set the CSRF token in the headers of AJAX requests
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        }
    });

    function issueBook() {
        var bookId = $('#id_book_id').val();  // Replace 'id_book_id' with the actual ID of your book input field
        $.ajax({
            url: '/issue_books/',
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')  // Make sure to have the getCookie function as described in the previous responses
            },
            success: function (data) {
                console.log('Book issued successfully:', data);
                // You can update the UI or perform additional actions after issuing a book
                alert('Book issued successfully!');
            },
            error: function (error) {
                console.error('Error issuing book:', error);
                alert('Error issuing book. Please try again.');
            }
        });
    }

// function issueBook() {
//         var selectedBookId = $('#book').val();
//         if (selectedBookId) {
//             $.ajax({
//                 url: `/issue_book/${selectedBookId}/`,
//                 method: 'POST',
//                 success: function (data) {
//                     console.log('Book issued successfully:', data);
//                     // You can update the UI or perform additional actions after issuing a book
//                 },
//                 error: function (error) {
//                     console.error('Error issuing book:', error);
//                 }
//             });
//         } else {
//             console.error('No book selected');
//         }
//     }