# coding=utf-8
# V1: 只测试marshmallow
from marshmallow import Schema, fields, post_load
from test.main_test1 import Player, compareResult, my_deserialize


class FriendSchema(Schema):
    fid = fields.Int()
    love = fields.Int()


class PlayerSchema(Schema):
    name = fields.Str()
    hp = fields.Float()
    lv = fields.Int()
    skills = fields.List(fields.Int())
    bag = fields.Dict(keys=fields.Str(), values=fields.Int())
    data = fields.List(fields.Int())
    dataMap = fields.Dict(keys=fields.Int(), values=fields.List(fields.Int()))
    bestFriend = fields.Nested(FriendSchema())
    friends = fields.List(fields.Nested(FriendSchema()))

    @post_load
    def make_object(self, data, **kwargs):
        return my_deserialize(Player, data)


print("------------- marshmallow -------------")
p = Player()
playerSchema = PlayerSchema()
result = playerSchema.dump(p)[0]  # python2.7中第二个位置存放错误信息
p1 = playerSchema.load(result)[0]
compareResult(p, p1)

