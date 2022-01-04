from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db import models
from django.utils.functional import SimpleLazyObject
from articlesapp.models import ArticlePost
from .forms import CommentForm
from .models import Comment
import random
import emoji

EMOJI_LIST = [':speak-no-evil_monkey:', ':monkey_face:', ':monkey:', ':dog_face:', ':dog:', ':poodle:', ':wolf:',
              ':cat_face:', ':grinning_cat:', ':grinning_cat_with_smiling_eyes:', ':pouting_cat:', ':cat:',
              ':tiger_face:', ':tiger:',  ':leopard:', ':horse_face:', ':horse:', ':cow_face:', ':ox:',
              ':water_buffalo:', ':cow:', ':pig_face:', ':pig:', ':boar:', ':pig_nose:', ':ram:', ':ewe:', ':goat:',
              ':camel:', ':elephant:', ':mouse_face:',  ':mouse:', ':rat:', ':hamster:', ':rabbit_face:', ':rabbit:',
              ':bear:', ':koala:', ':panda:', ':paw_prints:',  ':chicken:', ':rooster:', ':hatching_chick:',
              ':baby_chick:', ':front-facing_baby_chick:', ':bird:', ':penguin:', ':frog:', ':crocodile:', ':turtle:',
              ':snake:', ':dragon_face:', ':dragon:', ':spouting_whale:', ':whale:',  ':dolphin:', ':fish:',
              ':tropical_fish:', ':blowfish:', ':octopus:', ':spiral_shell:', ':snail:', ':bug:', ':ant:', ':honeybee:',
              ':lady_beetle:', ':butterfly:', ':boy:', ':girl:', ':man:', ':woman:', ':old_man:', ':old_woman:',
              ':baby:', ':person_blond_hair:', ':police_officer:', ':person_with_skullcap:', ':person_wearing_turban:',
              ':construction_worker:', ':princess:', ':guard:', ':Santa_Claus:', ':person_with_veil:', ':baby_angel:',
              ':person_getting_massage:', ':person_getting_haircut:', ':person_frowning:', ':person_pouting:',
              ':person_gesturing_NO:', ':person_gesturing_OK:', ':person_tipping_hand:', ':person_raising_hand:',
              ':person_bowing:', ':bust_in_silhouette:', ':busts_in_silhouette:', ':person_walking:',
              ':person_running:', ':people_with_bunny_ears:', ':woman_dancing:', ':woman_and_man_holding_hands:',
              ':men_holding_hands:', ':women_holding_hands:', ':kiss:', ':couple_with_heart:', ':family:', ':grapes:',
              ':melon:', ':watermelon:', ':tangerine:', ':lemon:', ':banana:', ':pineapple:', ':red_apple:',
              ':green_apple:', ':pear:', ':peach:', ':cherries:', ':strawberry:', ':bouquet:', ':cherry_blossom:',
              ':white_flower:', ':rose:', ':hibiscus:', ':sunflower:', ':blossom:', ':tulip:', ':seedling:',
              ':evergreen_tree:', ':deciduous_tree:', ':palm_tree:', ':cactus:', ':sheaf_of_rice:', ':herb:',
              ':four_leaf_clover:', ':maple_leaf:', ':fallen_leaf:', ':leaf_fluttering_in_wind:'
              ]


# Create your views here.
# 文章评论
# @login_required(login_url='/userprofile/login/')
def post_comment(request, article_id):
    # Model.objects.get()的功能基本是相同的
    article = get_object_or_404(ArticlePost, id=article_id)
    # 在show_article.html中设置了form表单，
    # 一旦提交就会触发action设置的url,comment:post_comment

    if request.method == 'POST':
        # 说明在进行了
        # tmp_comment = Comment.objects.create(article=article,
        #                                      critic=emoji.emojize(EMOJI_LIST[random.randint(0, len(EMOJI_LIST))]))
        # 处理 POST 请求
        # TODO 管理后台无法删除带有emoji表情的评论
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            # new_comment.user = request.user
            # 将用户随机的指定emoji
            new_comment. critic = EMOJI_LIST[random.randint(0, len(EMOJI_LIST))]
            new_comment.save()
            # redirect()：返回到一个适当的url中：即用户发送评论后，重新定向到文章详情页面。
            # 当其参数是一个Model对象时，会自动调用这个Model对象的get_absolute_url()方法
            # 因此需要在文章类里添加get_absolute_url
            return redirect(article)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 处理错误请求
    else:
        return HttpResponse("发表评论仅接受POST请求。")



