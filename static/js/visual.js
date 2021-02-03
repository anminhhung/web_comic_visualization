
$('#btn-loadfile').click(function () {
    var mode = document.getElementById("mode").value;
    var index = document.getElementById("number_id").value;
    var dataset = document.getElementById("choose_dataset").value;

    if (mode.localeCompare('index')==0){
        getImgFileName('index', index, dataset);
    }else if (mode.localeCompare('path')==0){
        getImgFileName('path', index, dataset);
    }
}
)

function getImgFileName(mode, index, dataset){
    $.ajax({
        url: 'get_img_name?mode='+mode+'&index='+index+'&dataset='+dataset,
        type: 'get',
        dataType: 'json',
        contentType: 'application/json',  
        success: function (response) {
            if (response['code'] == 1001) {
                alert("[Lỗi] Không nhận được phản hồi từ server, vui lòng kiểm tra lại!");
            }
            console.log(response);
            fname = response['data']['fname'];
            index = response['data']['index'];
            total = response['data']['total'];
            total_of_images = total;
            document.getElementById('number_id').value = index;
            var return_index = String(response['data']['index']);
            if (return_index.localeCompare('-1')==0){
                window.location.href = "idcard?mode=index&index=0";
            }
            drawImageOCR("/get_ori_img?dataset="+dataset+"&filename="+fname, fname, index);
            // loadLabel(fname, dataset);
        }
    }).done(function() {
        
    }).fail(function() {
        alert('Fail!');
    });
}

// function getImgFileName(){
//     drawImageOCR("/get_ori_img");
// }

function drawImageOCR(src) {
    var canvas = document.getElementById("preview_img");
    IMGSRC = src;
    var context = canvas.getContext('2d');
    var imageObj = new Image();
    imageObj.onload = function() {
        canvas.width = this.width;
        canvas.height = this.height;
        context.drawImage(imageObj, 0, 0, this.width,this.height);
    };
    imageObj.src = src;
}