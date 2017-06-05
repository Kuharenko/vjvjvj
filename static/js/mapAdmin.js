'use strict';

function MapAdmin() {
    Map.apply(this, arguments);

    this.markerTaskId = {};
    this.url.task = {
        action: '/task'
    };
    this.createMarkerByClick();
    this.submitTaskListener();
    this.deleteImageListener();
    this.showDate();
}

MapAdmin.prototype = Object.create(Map.prototype);

MapAdmin.prototype.createMarker = function () {
    var markerIndex = Map.prototype.createMarker.apply(this, arguments);
    var marker = this.markers[markerIndex];
    google.maps.event.addListener(marker, 'rightclick', this.removeMarker.bind(this, markerIndex));

    return markerIndex;
};

MapAdmin.prototype.deleteImageListener = function () {
    $('.wrap-map').on('click', function (e) {
        var $this = $(this);
        var target = $(e.target);
        var wrapImageElem = target.closest(".wrap-image");
        var closeElem = target.closest(".image-remove");

        if (wrapImageElem.length && closeElem.length) {
            //wrapImageElem.find("[name='existimg']").val('');
            wrapImageElem.remove();

            return false;
        }


    });
};

MapAdmin.prototype.submitTaskListener = function () {
    var $thisObj = this;
    $('.wrap-map').on('submit', function (e) {
        var $this = $(this);
        var formElem = e.target;
        var markerIndex = +formElem.index.value;
        var marker = $thisObj.markers[markerIndex];
        var pos = marker.getPosition();
        var formData = new FormData();
        var id = formElem.id.value;
        var type = undefined;
        var typeTask = formElem.type.value;

        formData.append("images", formElem.images.files);
        formData.append("title", formElem.title.value);
        formData.append("desc", formElem.desc.value);
        formData.append("type", typeTask);
        formData.append("pos", pos.lat() + ',' + pos.lng());

        var existimg = [].reduce.call($(formElem).find('[name="existimg"]'), function (a, elem) {
             var val = elem.value;
             if (val !== '') {
                 a.push(val);
             }
             return a;
        }, []).join(',');
        formData.append("existimg", existimg);

        if (id === '') {
            type = 'PUT';
        } else {
            type = 'POST';
            formData.append("id", id);
        }

        //var url = $thisObj.url.task;
        var url = '';
        if (id === '') {
            if (typeTask == 1) {
                url = '/admin/create/checkin'
            } else if (typeTask == 2) {
                url = '/admin/create/choice/'
            } else {
                url = '/admin/create/image/'
            }
        } else {
            if (typeTask == 1) {
                url = '/admin/edit/checkin/'
            } else if (typeTask == 2) {
                url = '/admin/edit/choice/'
            } else {
                url = '/admin/edit/image/'
            }

            url += id + '/';
        }

        var xhr = new XMLHttpRequest();
        xhr.open('POST', url);
        xhr.send(formData);

        xhr.onreadystatechange = function() {
            if (this.readyState != 4) return;

            if (xhr.status === 200 || xhr.status === 201) {
                var data = JSON.parse(this.responseText);

                if (id === '') {
                    $this.find('[name="id"]').val(data.id);
                    $thisObj.markerTaskId[markerIndex] = id;
                }

                $this.find('.message').removeClass('hidden danger').addClass('success').text('Задание успешно добавленно');
            } else {
                $this.find('.message').removeClass('hidden success').addClass('danger').text('Возникла ошибка:' + this.responseText);
            }
        };

        e.stopImmediatePropagation();
        e.preventDefault();
    });
};

MapAdmin.prototype.createMarkerByClick = function () {
    var $this = this;
    var map = this.map;

    google.maps.event.addListener(map, 'click', function(e) {
        $this.createMarker(true, {}, e.latLng);
    });
};

MapAdmin.prototype.createInfoWindow = function (taskData, markerIndex) {
    var marker = this.markers[markerIndex];

    var infoWindow = new google.maps.InfoWindow({
        content: this.createForm(taskData, markerIndex)
    });

    this.infoWindows.push(infoWindow);
    return infoWindow;
};

MapAdmin.prototype.createForm = function (taskData, markerIndex) {
    var html = '';

    html += '<div class="wrap-form-task">'
        + '<div class="message hidden"></div>'
        + '<form class="form-task">'
            + '<input type="hidden" name="id" value="' + (taskData.id === undefined ? '' : taskData.id) + '">'
            + '<input type="hidden" name="index" value="' + markerIndex + '">'
            + '<div><label>Название: <input type="text" name="title" value="' + (taskData.title === undefined ? '' : taskData.title) + '"/></label></div>'
            + '<div><label>Тип задания: <select name="type"><option ' + (taskData.type === undefined ? 'selected' : '') + ' disabled>Выберите задание</option>' +
                '<option ' + (taskData.type == 1 ? 'selected' : '') + ' value="1">Task 1</option>' +
                '<option ' + (taskData.type == 2 ? 'selected' : '') + ' value="2">Task 2</option>' +
                '<option ' + (taskData.type == 3 ? 'selected' : '') + ' value="3">Task 3</option>' +
            '</select></label></div>'
            + printCurrentImages(taskData.images)
            + '<div><label>Изображения: <input type="file" name="images" multiple></label></div>'
            + '<div><span>Описание: </span><textarea name="desc" rows="10" cols="50">' + (taskData.desc === undefined ? '' : taskData.desc) + '</textarea></div>'
            + '<div><button type="submit">Отправить</button></div>'
            + ''
        + '</form>'
        + '</div>';

    return html;

    function printCurrentImages(images) {
        var html = '';

        if (images && images.length) {
            html += '<div></div>';
            html += images.reduce(function (html, image) {
                html += '<span class="wrap-image">';
                html += '<input type="hidden" name="existimg" value="' + image + '">';
                html += '<img style="margin-right: 10px" src="' + image + '" height="50">';
                html += '<strong class="image-remove danger">x</strong>';
                html += '</span>';
                return html;
            }, html);
        }

        return html;
    }
};

MapAdmin.prototype.setNullMarker = function (markerIndex) {
    var marker = this.markers[markerIndex];
    marker.setMap(null);
    this.markers[markerIndex] = null;
};

MapAdmin.prototype.removeMarker = function (markerIndex) {
    var marker = this.markers[markerIndex];

    if (this.markerTaskId[markerIndex] !== undefined) {
        this.taskRemove(markerIndex);
    } else {
        this.setNullMarker(markerIndex);
    }
};

MapAdmin.prototype.taskRemove = function (markerIndex) {
    var $this = this;
    var id = this.markerTaskId[markerIndex];
    var marker = this.markers[markerIndex];
    var url = this.url.task;

    $.ajax({
        url: url.action,
        type: "DELETE"
    }).done(function (data) {
        $this.setNullMarker(markerIndex);
    }).fail(function (req) {
        alert('Произошла ошибка: ' + req.responseText);
    }).always(function () {
        
    })
};

MapAdmin.prototype.showDate = function () {
    var data = this.data;
    var $this = this;
    var createMarker = this.createMarker.bind(this, false);
    data.forEach(function(task){
        var markerIndex = createMarker(task);
        $this.markerTaskId[markerIndex] = task.id;
    });
};