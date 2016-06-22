// ***************************************** register.js functions *************************************
//    function goBack() {
//        window.history.back();
//    }
//
//    function prettyJson(json) {
//        return JSON.stringify(json)
//    }
//
//    function prettyJson(json) {
//        return JSON.stringify(json)
//    }
//
//    function minmax(){
//        alert(numrange);
//    }



// ************************** All other functions should be put in the $(document).ready(function()

$(document).ready(function(){


// ***********************************Limit amount of selected fields**********************************

    $('#fields').change(function(){
        if($('#fields option:selected').length >= 20){
            $('.ms-elem-selectable').prop('disabled', true);
            $('div.warning').css('color','red');

        } else {
            $('.ms-elem-selectable').prop('disabled', false);
        }
    })

// *********************************** Prevent Zero Fields from Being Submitted **********************************

//    $("form[name='fieldselect']").submit(function(stop){
//        if($('#fields option:selected').length == 0){
//            alert('Please Select at Least One Field.');
//            stop.preventDefault(stop);
//        }
//    })

// *******************************Search and Filter Fields****************************************

  $('#fields').multiSelect({
    selectableHeader: "<input type='text' class='search-input' autocomplete='off' placeholder='search'>",
    selectionHeader: "<input type='text' class='search-input' autocomplete='off' placeholder='search'>",
    afterInit: function(ms){
     var that = this,
            $selectableSearch = that.$selectableUl.prev(),
            $selectionSearch = that.$selectionUl.prev(),
            selectableSearchString = '#'+that.$container.attr('id')+' .ms-elem-selectable:not(.ms-selected)',
            selectionSearchString = '#'+that.$container.attr('id')+' .ms-elem-selection.ms-selected';

        that.qs1 = $selectableSearch.quicksearch(selectableSearchString)
        .on('keydown', function(e){
        if (e.which === 40){
         that.$selectableUl.focus();
         return false;
        }
        });

        that.qs2 = $selectionSearch.quicksearch(selectionSearchString)
        .on('keydown', function(e){
         if (e.which == 40){
            that.$selectionUl.focus();
            return false;
        }
        });
    },
    afterSelect: function(){
        this.qs1.cache();
        this.qs2.cache();
    },
    afterDeselect: function(){
        this.qs1.cache();
        this.qs2.cache();
    }

    });

// ********************************************* Table Pagination *******************************************

    $("#leadsTable").simplePagination({
        perPage: 10
    });

// ************************************* Detect is Browser Uses Input_Type:date ************************************

    if (!Modernizr.inputtypes.date) {
    $('input[type=date]').datepicker({
        // Consistent format with the HTML5 picker
        dateFormat: 'yy-mm-dd'
    });
}

// ************************************* Custom Fields Option Select ************************************

    $('#deselect_all').on('click', function(){
        $('#fields').multiSelect('deselect_all');
        return false
    });
    $('#deselect_all').on('click', function(){
        $('#fields').multiSelect('select', ['id']);
        return false;
    });


    $('#custom_default').click(function(){
        $('#fields').multiSelect('select', ['id', 'email', 'updatedAt', 'createdAt', 'firstName', 'lastName']);
        return false;
    });


    $("#save_fields").click(function(){
        var values = $("#fields>option:checked").map(function() { return $(this).val(); }).get();
        for (value of values){
            console.log(value)
        }
    });



// ******************************************* Compare Ranges ***************************************************





// **********************************************************************************************************

});

