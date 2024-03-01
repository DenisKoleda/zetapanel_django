$(document).ready(function(){
    // Event listener for form submission
    $('#searchForm').submit(function(e){
      e.preventDefault(); // Prevent the default form submission
      var query = $(this).find('input[name="task"]').val(); // Get the value of the input field
  
      $.ajax({
        url: '/tasks/', // URL to your Django view
        type: 'GET',
        data: { 'task': query },
        dataType: 'json',
        success: function(data) {
          updateTable(data.tasks); // Call updateTable with the returned tasks
        },
        error: function(xhr, status, error) {
          // Handle any errors here
          console.error("An error occurred: " + status + " " + error);
        }
      });
    });
  
    function updateTable(tasks) {
      var tableBody = $('.table tbody');
      tableBody.empty(); // Clear the current table body
  
      // Check if tasks are present
      if (tasks.length === 0) {
        //tableBody.append($('<tr>').append($('<td>').attr('colspan', '8').text('No tasks found.')));
      } else {
        // Iterate over the tasks and create new rows
        $.each(tasks, function(i, task){
          var row = $('<tr>').append(
            $('<td>').text(task.id),
            $('<td>').text(task.date),
            $('<td>').text(task.author),
            $('<td>').addClass('align-left text-start').text(task.ticket),
            $('<td>').text(task.priority),
            $('<td>').text(task.status),
            $('<td>').text(task.executor),
            // Add more task fields if necessary
          );
          tableBody.append(row);
        });
      }
    }
  });
  