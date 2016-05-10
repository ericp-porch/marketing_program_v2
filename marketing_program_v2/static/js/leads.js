// ***************************************** register.js functions *************************************
    function goBack() {
        window.history.back();
    }

    function prettyJson(json) {
        return JSON.stringify(json)
    }

    function prettyJson(json) {
        return JSON.stringify(json)
    }


// ************************** All other functions should be put in the $(document).ready(function()

$(document).ready(function(){


// ***********************************Limit amount of selected fields**********************************

    $('#fields').change(function(){
        if($('#fields option:selected').length >= 20){
            $('.ms-elem-selectable').prop('disabled', true);
            $("#warning").css("opacity") = "0.0";

        } else {
            $('.ms-elem-selectable').prop('disabled', false);
            $('#warning').css("opacity") = "1.0";
        }
    })

// ***********************************Return Selected Values**********************************
    $("form").submit(function(){
        myList = [];
        $('#fields option:selected').each(function() {
            myList.push($(this).val())
        });
        var data = myList
        var table = arrayToTable(data, {
                thead: false,
                attrs: {class: 'table'}
            })
        $('#printer').html(table);
    })

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

// *********************************  ************************************

});

