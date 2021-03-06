
import random
import emoji
import django.contrib.admin
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from articlesapp.models import ArticlePost

from mptt.models import MPTTModel, TreeForeignKey


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

# Create your models here.

# ???????????????
class Comment(models.Model):
    # article?????????????????????
    article = models.ForeignKey(
        ArticlePost,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    # # user?????????????????????
    # user = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     related_name='comments'
    # )
    # parent = TreeForeignKey(
    #     'self',
    #     on_delete=models.CASCADE,
    #     null=True,
    #     blank=True,
    #     related_name='children'
    # )
    # ???????????????????????????????????????, str
    # reply_to = models.ForeignKey(
    #     User,
    #     null=True,
    #     blank=True,
    #     on_delete=models.CASCADE,
    #     related_name='replyers'
    # )
    # critic?????????????????????
    critic = models.CharField(max_length=100, default='A')
    # body = models.TextField()
    # ???????????????????????????
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    # class MPTTMeta:
    #     order_insertion_by = ['created']

    def __str__(self):
        return self.body[:20]





