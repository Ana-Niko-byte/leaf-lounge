// const editButtons = document.getElementsByClassName("btn-edit");

// for (let button of editButtons){
//     button.addEventListener("click", (e) => {
//         e.preventDefault();
        
//         // Retrieve necessary parameter values.
//         const messageId = parseInt(button.dataset.messageId);
//         const forumSlug = document.getElementById("forum-slug").value;

//         console.log("Message ID:", messageId, typeof(messageId));  // Log message ID
//         console.log("Forum Slug:", forumSlug, typeof(forumSlug));  // Log forum slug

//         // Set message content into form.
//         let messageContent = document.getElementById(`message-content-${messageId}`).textContent;
//         document.getElementById("id_content").value = messageContent;

//         // Update button innerHTML text.
//         document.getElementById("message-send").innerHTML = "Update";

//         // Set action attribute to edit URL.
//         const messageForm = document.getElementById("messageForm");
//         const actionUrl = `/community/${forumSlug}/edit/${messageId}/`;
//         console.log("Action URL:", actionUrl);  // Log the final action URL
//         messageForm.setAttribute("action", actionUrl);
//     })
// };