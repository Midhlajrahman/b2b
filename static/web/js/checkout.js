const formattedDate = parsedDate.toLocaleDateString('en-US', {
    weekday: 'short',
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
  $('#id_selected-date').html(formattedDate);

  const totalPrice = $(".total-price");
    var adt_amt = 0;
    var child_amt = 0;
    var sum = 0;

    let countChild = 0;
    const countElementChild = $(".count-child");
    const countchild2 = $(".sum-child");
    const child_total = $("#child_total_price");
    const h_c_c = $("#h_child_count");
    

    const updateCountElementchild = () => {
      countElementChild.text(countChild);
      countchild2.text(countChild);
      countsummery.text(count);
      child_amt = countChild * child_price;
      sum = adt_amt + child_amt;
      child_total.html("= " + child_amt +" AED");
      totalPrice.text(sum + " AED");
    };

    countElementChild.text(countChild);

    const increaseCountChild = () => {
      countChild = Math.min(countChild + 1, datachilldMaxLimit);
      countElementChild.text(countChild);
      h_c_c.val(countChild);
      updateCountElementchild();
    };

    const decreaseCountChild = () => {
      countChild = Math.max(countChild - 1, 0);
      countElementChild.text(countChild);
      h_c_c.val(countChild);
      updateCountElementchild();
    };
    $(".increase-child").on("click", function (event) {
      event.preventDefault(); // Prevent form submission
      increaseCountChild();
    });

    $(".decrease-child").on("click", function (event) {
      event.preventDefault(); // Prevent form submission
      decreaseCountChild();
    });

    // Main count section
    let count = 0;
    const countElement = $(".count");
    const countsummery = $(".sum-count");
    const ad_total = $("#ad_total_price");
    const h_a_c = $("#h_ad_count");

    const updateCountElement = () => {
      countElement.text(count);
      countsummery.text(count);
      adt_amt = count * ad_price;
      sum = adt_amt + child_amt;
      ad_total.html("= " + adt_amt +" AED");
      totalPrice.text(sum + " AED");
    };

    const increaseCount = () => {
      count = Math.min(count + 1, dataMaxLimit);
      h_a_c.val(count);
      updateCountElement();
    };

    const decreaseCount = () => {
      count = Math.max(count - 1, 1);
      h_a_c.val(count);
      updateCountElement();
    };

    $(".increase").on("click", function (event) {
      event.preventDefault(); // Prevent form submission
      increaseCount();
    });

    $(".decrease").on("click", function (event) {
      event.preventDefault(); // Prevent form submission
      decreaseCount();
    });

    updateCountElement();

    $('.submit-btn').click(function(event) {
    
        var adultCount = parseInt($('#h_ad_count').val());
        var childCount = parseInt($('#h_child_count').val());
        if (!adultCount  && !childCount) {
          alert('Please select at least one adult or child.');
          event.preventDefault(); // Prevent form submission
        }
      });