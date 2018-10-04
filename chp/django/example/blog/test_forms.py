from chp.django.example.blog.forms import PostForm


def test_render():
    assert PostForm().render() == 'fail'
