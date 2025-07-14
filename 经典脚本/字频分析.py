from collections import Counter


def char_frequency(text):
    counter = Counter(text)
    total = sum(counter.values())

    print("字符\t数量\t占比(%)")
    print("-" * 20)
    for char, count in counter.most_common():
        percent = (count / total) * 100
        display_char = char if char != "\n" else "\\n"
        print(f"{display_char}\t{count}\t{percent:.2f}")


if __name__ == "__main__":
    content = """hA6h{8hGaGh}8B}ha6{hhha66}onnLan6Annh{F}6}an{}}onGo86h{n6hhaAnnn}6B66hA}8h8}oBGnhLBGAaoo6B}n}6hGa8G}oL}F68F6B}L6AG8nan6haG}}o8Go66BaaF6GBao6on8aFhnBF88oa6hLnoBa6}nG8n}GoA{6GhBnoAh8{ABnn6{}hhLFahGBonGBn6o}Fa6L}B{BBFh}nan6o}Bnah{}{B6a}aFnn}{B}a6G}nL}BB}no6GGh8{{888aonFBF88a}L}Fn6A}Gn8AB6n}n6aB8GA8n8o{on6aGh}Gnnn6}8a}BnaBaFhLGLB8A8nonhaoonoLLah}BGAh6aFon8haG{F8hL8}}}8oaa8}}GAF6GGL}ao6{G{AoF}FGa6An}6}6Bn}86hhoG8B{6}6A6nooo{h6hhohoa6nhoLL8}a{an8hGn{}F{BAaoFaB}FnAn66h{GLnBn6h}h8}h}}oFFBnB6ah}aoL{F6}BGhaoa8L8{L8aBh8Ga6nhh8hnBGn886F8h6nhan}}haB8BnoAAAa68}{66}aonohonLFa}Ah{h6{}aBn8LBGnnh{{G{onaa6GB6{nnBo}8{n{LnBoaa8F{a{hGGnaF{G{nohah}o8n8ahLaaL{{hLno}LnFGoGa{6AA8hLFh}AAGL}{ah{o66onn6hA{n8Goa68n6BoB{AAoFBa8{Gh}La8B}B6AFhnB{FG}Aa}oA6a{8a}B}o{{6annLn8FB{o68oAAa}Gho}{o}8n}668BA}BBAnBFahoana6LFa{B}G{}hFALLB6}nG8G}8o8ahA{{B6n}Bo8F}B{ha6naF}n6hha}}}6n}a6nhhh{hAaaa6}{Lohaon6}8AhA}8}8LLLoBnn{A88AnBoG}oGB{GG8}aLn{o8G8GB}G}{Ao8oGho}AAnA6BGh6GLB{hhAG6{6hha6hGhAGBnoF}6n{6Ga8aoah}AB8oBaaa6GFn{8{oB8GLah}{8}n6}a6}{6LGL6nn}h}8F6AL{A8FFn8na{aGnohGh86L6aoL{{}GLnaBhnn}naGa8n6L{h66o}oG{L}naGaaG88hL{6aFoo88FG}a}BAho}a68hBo8h}nLao{n}FLBLaaa}Aha6hBaL6h}FAnn6hBABahGBanG8oAGaB}G8hhhn}a}}A68An}B8A}a}anoGLFaG}FLF{LB}}8h{a6oGnLa}hnnaFBFB8FoGn}88on}hn}oaAhBah{a{6{8o}8oG}La}}Bo6h{}6}FhnB86BBnLaGLG6h6o}oahAA86aGBG6hhaLGn8hA{A8oALhohn{{B}F}LBo8L{Gn}hG{nF}8}8Anh6hBhB8na666hL{FnnoaAnBGF6{}nFnBnnnnGaAFhFBBALL6F}L}6{{8aAnh}aoF8}}{non68n{BA8oFLL6}AaALnnA}ha6{{onABonh}6h8anahon86L{LB{6ah}aa}FG}o8hn}hG}a}}8LhnB}o8L6nA}{hFBBoFn8FLFh}8G6A8}ooan6{Loo}}hhGh6hnnha{68}}noh}a66B6{}GBaAon}aooon6oahaha}FFn}L6B{onoA}oh8{6anA}LhaB}B6aG6{BanaaALoA}oG}onAnBB8A}nAL{Lahh}{6B}h{oBa8ananho{6Bnhonoo66nF8FBn{naBooh8h6nnaGo6oo}6aahan}{}Gho8{A8}hnBAoo6{a}}GhB}hABBnohG{66hA88GBn{AF}aaF}86Aa6L8h68LoaoF8}Bo8a}ah6}FFhGaLonB8{G}8Bo{A}AoALh8a6h}a}ALo8n{Ao}LA66B6BB"""
    char_frequency(content)




