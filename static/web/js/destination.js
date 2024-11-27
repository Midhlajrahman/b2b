var maxDateObj = new Date(max_validity_date);

var formattedMaxDate = $.datepicker.formatDate('mm/dd/yy', maxDateObj);
$('#id_validity_end_date').datepicker({
  dateFormat: 'mm/dd/yy',  
  minDate: 0, 
  maxDate: formattedMaxDate 
});
$('#id_check_availability').click(function () {
  const url = "/ticket/ajax_load_ticket/";
  var select_date = $("#id_validity_end_date").val();
  if (!select_date) {
    alert("Please Select Date");
  }
  if (select_date) {
    $.ajax({
      url: url,
      data: {
        'select_date': select_date,
        'destination': destination
      },
      success: function (data) {
        if (data.instance ) {
          const parsedDate = new Date(data.select_date);
          const formattedDate = parsedDate.toLocaleDateString('en-US', {
            weekday: 'short',
            year: 'numeric',
            month: 'short',
            day: 'numeric',
          });
          $("#id_tickets").html(
            `<div class="row y-gap-30 pt-40">
              <div class="col-12">
                <div class="px-24 py-20 rounded-16 bg-green-1">
                  <div class="row x-gap-20 y-gap-20 items-center">
                    <h4 class=" text-18 lh-15 fw-500" style="font-size: 18px !important;padding-bottom: 0;">${destination_name}</h4>
                    <p style="font-size: 13px !important;padding-top: 0;">${formattedDate}</p>
                    <form  method="get" action="/ticket/checkout/${data.order_id}/">
                    
                    <input type="hidden" name="destination" value="${data.destination}">
                    <input type="hidden" name="guist_count" value="${data.guist_count}">
                    <input type="hidden" name="child_count" value="${data.child_count}">
                    <input type="hidden" name="select_date" value="${data.select_date}">
                    
                    <button type="submit"  class="button h-50 px-24 -dark-1 bg-blue-1 text-white" style="margin: 0px 10px 10px 10px;width: 95%;">
                        Next <div class="icon-arrow-top-right ml-15"></div>
                    </button>
                    </form>
                  </div>
                </div>
              </div>
            </div>
          `);
          
        }
        else {
          $("#id_tickets").html(
            `<div class="row y-gap-30 pt-40">
              <div class="col-12">
                <div class="px-24 py-20 rounded-4 bg-green-1">
                  <div class="row x-gap-20 y-gap-20 items-center">
                    <h4 class="mt-10 text-18 lh-15 fw-500">Tickets Not Available</h4>
                  </div>
                </div>
              </div>
            </div>
          `);
        }
        
      }
    });
  }
  
});

// const maxDateObj = new Date(max_validity_date);
// const formattedMaxDate = $.datepicker.formatDate('mm/dd/yy', maxDateObj);

// $('#id_validity_end_date').datepicker({
//   dateFormat: 'mm/dd/yy',
//   minDate: 0,
//   maxDate: formattedMaxDate
// });

// $('#id_check_availability').click(function () {
//   const url = "/ticket/ajax_load_ticket/";
//   const select_date = $("#id_validity_end_date").val();

//   if (!select_date) {
//     alert("Please Select Date");
//     return; // Exit the function if no date is selected
//   }

//   $.ajax({
//     url: url,
//     data: {
//       'select_date': select_date,
//       'destination': destination
//     },
//     success: function (data) {
//       $("#id_tickets").html(''); // Clear previous results

//       if (data.instance) {
//         const parsedDate = new Date(data.select_date);
//         const formattedDate = parsedDate.toLocaleDateString('en-US', {
//           weekday: 'short',
//           year: 'numeric',
//           month: 'short',
//           day: 'numeric',
//         });

//         $("#id_tickets").html(`
//           <div class="row y-gap-30 pt-40">
//             <div class="col-12">
//               <div class="px-24 py-20 rounded-16 bg-green-1">
//                 <div class="row x-gap-20 y-gap-20 items-center">
//                   <h4 class="text-18 lh-15 fw-500" style="font-size: 18px !important;padding-bottom: 0;">${destination_name}</h4>
//                   <p style="font-size: 13px !important;padding-top: 0;">${formattedDate}</p>
//                   <form method="get" action="/ticket/checkout/${data.order_id}/">
//                     <input type="hidden" name="destination" value="${data.destination}">
//                     <input type="hidden" name="guist_count" value="${data.guist_count}">
//                     <input type="hidden" name="child_count" value="${data.child_count}">
//                     <input type="hidden" name="select_date" value="${data.select_date}">
//                     <button type="submit" class="button h-50 px-24 -dark-1 bg-blue-1 text-white" style="margin: 0px 10px 10px 10px;width: 95%;">
//                       Next <div class="icon-arrow-top-right ml-15"></div>
//                     </button>
//                   </form>
//                 </div>
//               </div>
//             </div>
//           </div>
//         `);
//       } else {
//         $("#id_tickets").html(`
//           <div class="row y-gap-30 pt-40">
//             <div class="col-12">
//               <div class="px-24 py-20 rounded-4 bg-green-1">
//                 <div class="row x-gap-20 y-gap-20 items-center">
//                   <h4 class="mt-10 text-18 lh-15 fw-500">Tickets Not Available</h4>
//                 </div>
//               </div>
//             </div>
//           </div>
//         `);
//       }
//     }
//   });
// });