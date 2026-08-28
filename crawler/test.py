from crawler.client import get_artists, get_artistdetail, get_artistintro, _sleep


TEST_NAME = "郑润泽"


def test_artist_intro():

    print("=" * 60)
    print(f"测试歌手：{TEST_NAME}")
    print("=" * 60)

    try:
        # 搜索歌手
        data = get_artists(TEST_NAME, 1)

        artist_list = data.get("result", {}).get("artists", [])

        print(f"搜索结果数量：{len(artist_list)}")

        if not artist_list:
            print("没有找到歌手")
            return

        for artist in artist_list[:5]:
            print(
                f"ID={artist.get('id')} | "
                f"姓名={artist.get('name')}"
            )

        # 找到名字完全匹配的歌手
        target = None

        for artist in artist_list:
            if artist.get("name") == TEST_NAME:
                target = artist
                break

        if target is None:
            print("没有找到名字完全匹配的歌手")
            return

        artist_id = target.get("id")

        print("\n" + "=" * 60)
        print("测试详情接口")
        print("=" * 60)

        detail = get_artistdetail(artist_id)

        print("artist_id：", artist_id)
        print("artist_name：", detail.get("name"))
        print("artist_image：", detail.get("picUrl"))

        _sleep()

        print("\n" + "=" * 60)
        print("测试简介接口")
        print("=" * 60)

        intro = get_artistintro(artist_id)

        print("返回类型：", type(intro).__name__)
        print("简介长度：", len(intro) if intro else 0)
        print("简介原始内容：")
        print(repr(intro))

        if intro and intro.strip():
            print("\n结论：接口返回了简介")
        else:
            print("\n结论：接口没有返回简介")

    except Exception as e:
        print("测试失败：", repr(e))


if __name__ == "__main__":
    test_artist_intro()
