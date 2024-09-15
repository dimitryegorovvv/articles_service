$(document).ready(function() {
    function check_form_create_article(event) {
        event.preventDefault(); 

        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const form = $(this);
        const title = $('.create_article_name').val();
        const text = $('.create_article_text').val();
        let formIsValid = true;

        if (title.length < 3){
            $('.title_error').css('display', 'block');
            formIsValid = false;
        } else {
            $('.title_error').css('display', 'none');
        }

        if (text.length < 10){
            $('.text_error').css('display', 'block');
            formIsValid = false;
        } else {
            $('.text_error').css('display', 'none');
        }

        if (formIsValid) {
            const formData = new FormData(form[0]);
            formData.append('csrfmiddlewaretoken', csrftoken);

            $.ajax({
                url: form.attr('action'),
                type: 'POST',
                data: formData,
                contentType: false, // Не устанавливать заголовок Content-Type
                processData: false, // Не преобразовывать данные
                success: function() {
                    timeout_sending(del_text=true);
                    $('.art_published').css('display', 'block');
                    $('.create_article_name').val('');
                    $('.create_article_text').val('');
                    $('input[name="article_image"]').val(''); // Очистить поле изображения
                },
                error: function() {
                    alert("Произошла ошибка, попробуйте позже");
                }
            });
        }
    }
    
    $('form.create_article_form').submit(check_form_create_article);
});



$(document).ready(function() {
    function send_comment(event) {
        event.preventDefault(); 

        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const form = $(this);
        const text = $('.ta_comment').val();

        let formIsValid = true;

        if (text.length < 1){
            formIsValid = false;
        }

        if (formIsValid) {
            $.ajax({
                url: form.attr('action'),
                type: 'POST',
                data: $(this).serialize(),
                success: function(data) {
                    if (data.user_is_not_auth) {
                        $('.need_auth').text(data.user_is_not_auth)
                    } else {
                        $('.ta_comment').val('');
                        if (data.error) {
                            alert(data.error);
                        } else {
                            $('.need_auth').text('');
                            $('.comments_wr').prepend(
                                '<div class="comment">' +
                                '<div class="comment_text">' + data.text + '</div>' +
                                '<div class="comm_a_d">' +
                                '<div class="comment_author">' + data.author + '</div>' +
                                '<div class="comment_date">' + data.created_at + '</div>' +
                                '</div></div>'
                            );
                        }
                    }
                    
                },
                error: function() {
                    alert("Произошла ошибка, попробуйте позже");
                }
            });
        }
    }
    
    $('form.form_comment').submit(send_comment);
});


// timer //
let timer; 
let typing = false;  
let typingTimeout;  

function timeout_sending(del_text=false) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    if (del_text){
        text='';
    }else{
        text = $('.create_article_text').val();
    }
    $.ajax({
        url: '/save_text/',
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': csrftoken,
            'text': text,
        },
        success: function() {
        },
        error: function() {
        }
    });
}

function startSending() {
    if (!timer) {  
        timer = setInterval(timeout_sending, 5000);
        timeout_sending();  
    }
}

function stopSending() {
    clearInterval(timer);
    timer = null;
    typing = false;  
}

$('.create_article_text').bind('input', function() {
    if ($('.create_article_text').val() == ''){
        timeout_sending(del_text=true);
    }
    if (!typing) {  
        typing = true;
        startSending();
    }

    clearTimeout(typingTimeout);
    typingTimeout = setTimeout(stopSending, 5000);
});
// timer //


$(document).ready(function() {
    if ($('form').hasClass('create_article_form')) {
        var textFromServer = $('form').data('text');
        $('.create_article_text').val(textFromServer);
    }
});



$(document).ready(function() {
    function publish_article(event) {
        event.preventDefault(); 

        var article_id = $(this).find('button').data('article-id'); 
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const form = $(this);

        $.ajax({
            url: form.attr('action'),
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrftoken, 
                'article_id': article_id,
            },
            success: function() {
                form.parent().remove();
            },
            error: function() {
                alert("Произошла ошибка, попробуйте позже");
            }
        });
    }
    
    $('form.form_but_pan').submit(publish_article);
});


$(document).ready(function() {
    function del_article(event) {
        event.preventDefault(); 

        var article_id = $(this).find('button').data('article-id'); 
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const form = $(this);

        $.ajax({
            url: form.attr('action'),
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrftoken, 
                'article_id': article_id,
            },
            success: function() {
                form.parent().remove();
            },
            error: function() {
                alert("Произошла ошибка, попробуйте позже");
            }
        });
    }
    
    $('form.form_del_art').submit(del_article);
});


$('.btn_edit_art').on('click', function() {
    let art_text = $('.article_text').data('article-text');

    $('.article_text').css('display', 'none');
    $('.img_art').after('<textarea name="article_text_edit" class="ta_edit"></textarea>');
    $('.ta_edit').val(art_text);
    $('.btn_edit_art').css('display', 'none');
    $('.form_edit_art').css('display', 'block');
    $('.suc_edit').remove();
});


$(document).ready(function() {
    function edit_article(event) {
        event.preventDefault();

        var article_id = $(this).find('button').data('article-id'); 
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const form = $(this);
        const text = $('.ta_edit').val();

        $.ajax({
            url: form.attr('action'),
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'article_id': article_id,
                'text': text,   
            },
            success: function(response) {
                $('.ta_edit').css('display', 'none');
                $('.article_text').css('display', 'block');
                $('.form_edit_art').css('display', 'none');
                $('.btn_edit_art').css('display', 'block');
                $('.article_text').text(response.article_new_text);
                $('.home_art_title').after('<div class="suc_edit">Изменения успешно сохранены</div>');
            },
            error: function() {
                alert("Произошла ошибка, попробуйте позже");
            }
        });
    }
    
    $('form.form_edit_art').submit(edit_article);
});