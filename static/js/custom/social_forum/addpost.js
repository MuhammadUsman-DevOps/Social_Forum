// "use strict";
// var uploadPost = function () {
//     var text_content = $('#kt_forms_widget_1_editor').text();
//     var data = new FormData();
//     data.append("csrfmiddlewaretoken", "{{ csrf_token }}")
//     data.append("text_content", text_content);
//     data.append("post_media", $("input[id^='post_pic']")[0].files[0]);
//
//     $.ajax(
//         {
//             url: '{% url 'upload_post' %}',
//             type: "POST",
//             processData: false,
//             contentType: false,
//             mimetype: "multipart/form-data",
//             data: data,
//             datatype: 'JSON',
//             success: function (response) {
//                 console.log(response);
//                 $('#newsFeed_section').prepend(response)
// // {#TODO after posting refresh the post content area#}
//                 $("#kt_forms_widget_1_editor").load(window.location.href + " #kt_forms_widget_1_editor");
//
//             }
//         }
//     );
// }

