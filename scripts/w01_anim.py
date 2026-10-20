"""1주차 「여러 가지 순열」 manim 애니메이션.

렌더링: python scripts/render_w01.py
"""
from itertools import permutations

import numpy as np
from manim import *

config.background_color = WHITE

FONT = "Malgun Gothic"
INK = "#1d2433"
SUB = "#5b6475"
LINE = "#d5dae3"
BLUE = "#2f6fde"
BLUE_SOFT = "#dce8fb"
RED = "#e0533d"
RED_SOFT = "#fbe1dc"
GOLD = "#f2b632"
GOLD_SOFT = "#fdf0cf"


def T(s, size=36, color=INK, weight=NORMAL):
    return Text(s, font=FONT, font_size=size, color=color, weight=weight)


def person(label, color=BLUE, r=0.42, size=30):
    c = Circle(radius=r, fill_color=color, fill_opacity=1, stroke_color=WHITE, stroke_width=4)
    return VGroup(c, T(label, size, WHITE, BOLD).move_to(c))


def table(center, r=1.3):
    return Circle(radius=r, fill_color=GOLD_SOFT, fill_opacity=1, stroke_color=GOLD, stroke_width=6).move_to(center)


def seat(center, R, i, n, offset=0.0):
    a = PI / 2 - i * TAU / n - offset
    return center + R * np.array([np.cos(a), np.sin(a), 0])


def label_box(s, w=1.3, h=0.55, size=26, fill=WHITE, stroke=LINE, color=INK):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.1, fill_color=fill, fill_opacity=1, stroke_color=stroke, stroke_width=3)
    return VGroup(r, T(s, size, color, BOLD).move_to(r))


def mini_circle(s, center, r=0.3):
    g = VGroup(Circle(radius=r, stroke_color=GOLD, stroke_width=3, fill_color=GOLD_SOFT, fill_opacity=1).move_to(center))
    for i, ch in enumerate(s):
        p = seat(center, r + 0.05, i, len(s))
        dot = Circle(radius=0.15, fill_color=RED if ch == "A" else BLUE, fill_opacity=1, stroke_width=0).move_to(p)
        g.add(VGroup(dot, T(ch, 15, WHITE, BOLD).move_to(dot)))
    return g


def tile(ch, idx=None, s=0.6):
    soft, col = (BLUE_SOFT, BLUE) if ch == "a" else (RED_SOFT, RED)
    sq = RoundedRectangle(width=s, height=s, corner_radius=0.08, fill_color=soft, fill_opacity=1, stroke_color=col, stroke_width=3)
    g = VGroup(sq, T(ch, int(s * 50), col, BOLD).move_to(sq).shift(LEFT * 0.05 * (idx is not None)))
    if idx is not None:
        g.add(T(str(idx), int(s * 26), col, BOLD).move_to(sq.get_corner(DR) + np.array([-0.13, 0.15, 0]) * s / 0.6))
    return g


def tile_row(chars, idxs=None, s=0.6, gap=0.08):
    idxs = idxs or [None] * len(chars)
    return VGroup(*[tile(c, i, s) for c, i in zip(chars, idxs)]).arrange(RIGHT, buff=gap)


class CircleRotate(Scene):
    """원탁을 회전해도 같은 배열임을 보여 주는 장면"""

    def construct(self):
        center = LEFT * 3.2 + DOWN * 0.1
        R = 2.0
        tbl = table(center)
        labels = "ABCD"
        theta = ValueTracker(0)
        people = VGroup()
        for i, l in enumerate(labels):
            p = person(l, RED if l == "A" else BLUE)
            p.add_updater(lambda m, i=i: m.move_to(seat(center, R, i, 4, theta.get_value())))
            people.add(p)

        reading = label_box("ABCD", w=1.8, h=0.7, size=34, fill=BLUE_SOFT, stroke=BLUE, color=BLUE).move_to(center + DOWN * 3.15)
        head = T("위에서부터 시계 방향으로 읽기", 28, SUB).move_to(RIGHT * 3.4 + UP * 3.1)
        slots = [RIGHT * 3.4 + UP * (2.0 - k * 1.0) for k in range(4)]

        self.play(FadeIn(tbl), LaggedStart(*[GrowFromCenter(p) for p in people], lag_ratio=0.2))
        self.play(FadeIn(reading, shift=UP * 0.2), FadeIn(head))
        entries = VGroup(label_box("ABCD", w=1.8, h=0.7, size=32).move_to(slots[0]))
        self.play(TransformFromCopy(reading, entries[0]))

        for k in range(1, 4):
            s = labels[-k:] + labels[:-k]
            self.play(theta.animate.set_value(k * PI / 2), run_time=1.2)
            new_reading = label_box(s, w=1.8, h=0.7, size=34, fill=BLUE_SOFT, stroke=BLUE, color=BLUE).move_to(reading)
            self.play(Transform(reading, new_reading), run_time=0.4)
            e = label_box(s, w=1.8, h=0.7, size=32).move_to(slots[k])
            entries.add(e)
            self.play(TransformFromCopy(reading, e), run_time=0.6)

        frame = SurroundingRectangle(entries, color=BLUE, buff=0.2, stroke_width=5)
        res = T("원형으로는 모두 같은 1가지", 34, BLUE, BOLD).next_to(frame, DOWN, buff=0.35)
        self.play(Create(frame), Write(res))
        self.play(theta.animate.set_value(TAU), run_time=1.5)
        self.wait(1.5)


class CircleCount(Scene):
    """일렬 배열 24가지가 원순열 6가지로 묶이는 장면"""

    def construct(self):
        title = T("4명을 일렬로 세우는 경우  4! = 24", 32, INK, BOLD).to_corner(UL, buff=0.45)
        rows = VGroup()
        for k, p in enumerate(permutations("BCD")):
            s = "A" + "".join(p)
            row = VGroup(*[
                label_box(s[j:] + s[:j], w=1.3, h=0.55, size=24,
                          fill=BLUE_SOFT if j == 0 else WHITE, stroke=BLUE if j == 0 else LINE,
                          color=BLUE if j == 0 else INK)
                for j in range(4)
            ]).arrange(RIGHT, buff=0.15)
            rows.add(row)
        rows.arrange(DOWN, buff=0.42).move_to(LEFT * 3.6 + DOWN * 0.45)

        self.play(Write(title))
        self.play(LaggedStart(*[FadeIn(b, scale=0.8) for row in rows for b in row], lag_ratio=0.05), run_time=2.5)
        self.wait(0.5)

        note = T("한 줄 = 회전하면 같은 4가지", 26, SUB).move_to(RIGHT * 4.2 + UP * 1.8)
        self.play(FadeIn(note))
        circles = VGroup()
        for k, row in enumerate(rows):
            s = row[0][1].text
            box = SurroundingRectangle(row, color=BLUE, buff=0.07, stroke_width=4)
            mc = mini_circle(s, np.array([0.45, row.get_center()[1], 0]), r=0.27)
            circles.add(mc)
            self.play(Create(box), TransformFromCopy(row, mc), run_time=0.7 if k < 2 else 0.45)
            self.play(FadeOut(box), run_time=0.2)

        eq1 = T("24 ÷ 4 = 6", 54, INK, BOLD).move_to(RIGHT * 4.0 + UP * 0.6)
        eq2 = T("= 3! = (4 − 1)!", 44, BLUE, BOLD).next_to(eq1, DOWN, buff=0.45)
        brace = Brace(circles, RIGHT, color=BLUE)
        self.play(GrowFromCenter(brace), Write(eq1))
        self.play(Write(eq2))
        self.play(Circumscribe(eq2, color=BLUE))
        self.wait(1.5)


class Adjacent(Scene):
    """이웃하는 두 사람을 한 묶음으로 보는 장면"""

    def construct(self):
        center = LEFT * 3.2 + DOWN * 0.2
        R = 2.0
        tbl = table(center, 1.2)
        names = ["회", "부", "C", "D", "E"]
        ppl = {n: person(n, RED if n in "회부" else BLUE) for n in names}
        for i, n in enumerate(names):
            ppl[n].move_to(seat(center, R, i, 5))

        t1 = T("5명이 원탁에 앉는 경우", 30, SUB).move_to(RIGHT * 3.4 + UP * 2.4)
        e1 = T("(5 − 1)! = 24", 44, INK, BOLD).next_to(t1, DOWN, buff=0.3)
        self.play(FadeIn(tbl), LaggedStart(*[GrowFromCenter(ppl[n]) for n in names], lag_ratio=0.15))
        self.play(FadeIn(t1), Write(e1))
        self.wait(0.8)

        # 회장·부회장을 묶어서 4자리로 재배치
        top = seat(center, R + 0.1, 0, 4)
        pill = RoundedRectangle(width=2.0, height=1.05, corner_radius=0.52, fill_color=RED_SOFT, fill_opacity=1,
                                stroke_color=RED, stroke_width=4).move_to(top)
        t2 = T("회장·부회장을 한 묶음으로", 30, RED, BOLD).move_to(RIGHT * 3.4 + UP * 0.9)
        e2 = T("(4 − 1)! = 6", 44, INK, BOLD).next_to(t2, DOWN, buff=0.3)
        self.play(
            FadeIn(pill),
            ppl["회"].animate.move_to(top + LEFT * 0.48),
            ppl["부"].animate.move_to(top + RIGHT * 0.48),
            ppl["C"].animate.move_to(seat(center, R, 1, 4)),
            ppl["D"].animate.move_to(seat(center, R, 2, 4)),
            ppl["E"].animate.move_to(seat(center, R, 3, 4)),
            t1.animate.set_opacity(0.35), e1.animate.set_opacity(0.35),
            run_time=1.5,
        )
        self.bring_to_front(ppl["회"], ppl["부"])
        self.play(FadeIn(t2), Write(e2))
        self.wait(0.6)

        t3 = T("묶음 안에서 자리 바꿈", 30, RED, BOLD).move_to(RIGHT * 3.4 + DOWN * 0.6)
        e3 = T("2! = 2", 44, INK, BOLD).next_to(t3, DOWN, buff=0.3)
        self.play(FadeIn(t3))
        self.play(Swap(ppl["회"], ppl["부"]), run_time=1.0)
        self.play(Write(e3))
        self.play(Swap(ppl["회"], ppl["부"]), run_time=1.0)

        res = label_box("6 × 2 = 12", w=4.2, h=1.1, size=50, fill=BLUE_SOFT, stroke=BLUE, color=BLUE).move_to(RIGHT * 3.4 + DOWN * 2.9)
        self.play(FadeIn(res, scale=0.8))
        self.play(Circumscribe(res, color=BLUE))
        self.wait(1.5)


class Repeated(Scene):
    """중복순열: 비밀번호 다이얼과 비트 트리"""

    def construct(self):
        # 1) 세 자리 비밀번호
        title = T("세 자리 비밀번호: 자리마다 0~9", 34, INK, BOLD).to_edge(UP, buff=0.5)
        body = RoundedRectangle(width=8.0, height=3.4, corner_radius=0.4, fill_color="#f4f6fa", fill_opacity=1,
                                stroke_color=INK, stroke_width=4).shift(DOWN * 0.1)
        shackle = Arc(radius=1.6, start_angle=0, angle=PI, stroke_color=INK, stroke_width=22).next_to(body, UP, buff=-0.05)
        trackers = [ValueTracker(0) for _ in range(3)]
        dials = VGroup()
        for k, tr in enumerate(trackers):
            x = (k - 1) * 2.3
            box = RoundedRectangle(width=1.5, height=1.9, corner_radius=0.15, fill_color=WHITE, fill_opacity=1,
                                   stroke_color=BLUE, stroke_width=5).move_to([x, 0.15, 0])
            num = always_redraw(lambda tr=tr, box=box: T(str(int(tr.get_value()) % 10), 80, BLUE, BOLD).move_to(box))
            cap = T("10가지", 28, SUB, BOLD).next_to(box, DOWN, buff=0.2)
            dials.add(VGroup(box, num, cap))
        self.play(Write(title), FadeIn(body), Create(shackle))
        self.play(LaggedStart(*[FadeIn(d) for d in dials], lag_ratio=0.2))
        self.play(*[tr.animate.set_value(v) for tr, v in zip(trackers, [13, 20, 17])], run_time=2.5, rate_func=linear)
        eq = T("10 × 10 × 10 = 10³ = 1000가지", 44, INK, BOLD).to_edge(DOWN, buff=0.5)
        self.play(Write(eq))
        self.wait(1.2)
        self.play(*[FadeOut(m) for m in [title, body, shackle, dials, eq]])

        # 2) 비트가 늘 때마다 2배가 되는 트리
        title2 = T("n비트 신호: 비트마다 0 또는 1", 34, INK, BOLD).to_corner(UL, buff=0.45)
        self.play(Write(title2))
        root = Dot([-5.6, -0.3, 0], radius=0.12, color=INK)
        self.play(FadeIn(root))
        xs = [-3.6, -1.6, 0.4]
        prev = [root.get_center()]
        side = VGroup()
        texts = ["1비트: 2", "2비트: 2 × 2 = 4", "3비트: 2 × 2 × 2 = 8"]
        for L in range(3):
            n = 2 ** (L + 1)
            gap = 5.8 / n
            ys = [2.6 - gap * (k + 0.5) for k in range(n)]
            nodes, edges = VGroup(), VGroup()
            for k in range(n):
                p = np.array([xs[L], ys[k], 0])
                parent = prev[k // 2]
                bit = k % 2
                edges.add(Line(parent, p, color=LINE, stroke_width=4).set_z_index(-1))
                c = Circle(radius=0.27, fill_color=BLUE_SOFT if bit else WHITE, fill_opacity=1,
                           stroke_color=BLUE if bit else INK, stroke_width=3).move_to(p)
                nodes.add(VGroup(c, T(str(bit), 26, BLUE if bit else INK, BOLD).move_to(c)))
            cnt = T(f"{n}가지", 26, BLUE, BOLD).move_to([xs[L], -3.6, 0])
            line = T(texts[L], 30, INK).move_to([4.6, 1.6 - L * 0.8, 0])
            self.play(Create(edges), LaggedStart(*[GrowFromCenter(nd) for nd in nodes], lag_ratio=0.05), run_time=1.2)
            self.play(FadeIn(cnt), FadeIn(line, shift=LEFT * 0.2))
            side.add(line)
            prev = [nd.get_center() for nd in nodes]
        dots = T("⋮", 34, SUB).move_to([4.6, -0.75, 0])
        final = label_box("8비트: 2⁸ = 256", w=4.4, h=0.95, size=38, fill=BLUE_SOFT, stroke=BLUE, color=BLUE).move_to([4.6, -1.8, 0])
        self.play(FadeIn(dots))
        self.play(FadeIn(final, scale=0.8))
        self.play(Circumscribe(final, color=BLUE))
        self.wait(1.5)


class SameThings(Scene):
    """같은 것이 있는 순열: 첨자를 지우면 겹치는 배열"""

    def construct(self):
        top = tile_row("aaabb", [1, 2, 3, 1, 2], s=0.7).move_to(LEFT * 3.4 + UP * 2.9)
        t1 = T("모두 다르다고 보면  5! = 120가지", 32, INK, BOLD).next_to(top, RIGHT, buff=0.6)
        self.play(LaggedStart(*[FadeIn(x, shift=DOWN * 0.2) for x in top], lag_ratio=0.1))
        self.play(Write(t1))

        pattern = "abaab"
        rows = VGroup()
        for pa in permutations([1, 2, 3]):
            for pb in permutations([1, 2]):
                ia, ib = iter(pa), iter(pb)
                rows.add(tile_row(pattern, [next(ia) if c == "a" else next(ib) for c in pattern], s=0.5, gap=0.06))
        rows.arrange_in_grid(rows=4, cols=3, buff=(0.8, 0.3)).move_to(DOWN * 0.3)
        t2 = T("첨자만 다른 12가지 = 3! × 2!", 30, SUB).next_to(rows, UP, buff=0.3)
        self.play(FadeIn(t2), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.08), run_time=2.0)
        self.wait(0.6)

        plain = tile_row(pattern, s=0.8).move_to(DOWN * 0.3)
        t3 = T("첨자를 지우면 모두 같은 1가지", 32, BLUE, BOLD).next_to(plain, DOWN, buff=0.5)
        self.play(*[ReplacementTransform(r, plain.copy()) for r in rows], FadeOut(t2), run_time=1.5)
        self.add(plain)
        self.play(Write(t3))
        eq = label_box("120 ÷ (3! × 2!) = 120 ÷ 12 = 10", w=9.2, h=1.0, size=40, fill=BLUE_SOFT, stroke=BLUE, color=BLUE).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(eq, scale=0.9))
        self.wait(1.2)

        self.play(*[FadeOut(m) for m in self.mobjects])
        title = T("a 3개, b 2개를 나열하는 10가지", 34, INK, BOLD).to_edge(UP, buff=0.5)
        allrows = VGroup()
        for i in range(5):
            for j in range(i + 1, 5):
                allrows.add(tile_row("".join("b" if k in (i, j) else "a" for k in range(5)), s=0.6))
        allrows.arrange_in_grid(rows=5, cols=2, buff=(1.2, 0.3)).next_to(title, DOWN, buff=0.5)
        self.play(Write(title))
        self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.15) for r in allrows], lag_ratio=0.12), run_time=2.0)
        self.wait(1.5)


class ShortestPath(Scene):
    """격자의 최단 경로 = a, b 문자열 / 각 점까지의 경로 수"""

    def construct(self):
        s = 1.25
        O = np.array([-6.0, -1.6, 0])
        P = lambda i, j: O + np.array([i * s, j * s, 0])
        grid = VGroup(*[Line(P(i, 0), P(i, 2), color=LINE, stroke_width=4) for i in range(5)],
                      *[Line(P(0, j), P(4, j), color=LINE, stroke_width=4) for j in range(3)])
        A = VGroup(Dot(P(0, 0), radius=0.13, color=INK), T("A", 34, INK, BOLD).next_to(P(0, 0), DL, buff=0.35))
        B = VGroup(Dot(P(4, 2), radius=0.13, color=INK), T("B", 34, INK, BOLD).next_to(P(4, 2), UR, buff=0.35))
        legend = VGroup(T("오른쪽 한 칸 → a", 30, BLUE, BOLD), T("위쪽 한 칸 ↑ b", 30, RED, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        legend.move_to(RIGHT * 3.5 + UP * 2.4)
        self.play(Create(grid), FadeIn(A), FadeIn(B))
        self.play(FadeIn(legend))

        def walk(moves, fast=False):
            i = j = 0
            segs, letters = VGroup(), VGroup()
            for k, m in enumerate(moves):
                ni, nj = (i + 1, j) if m == "a" else (i, j + 1)
                seg = Line(P(i, j), P(ni, nj), color=BLUE if m == "a" else RED, stroke_width=12)
                t = tile(m, s=0.55).move_to(O + np.array([k * 0.65 + 0.3, -1.1, 0]))
                self.play(Create(seg), FadeIn(t, shift=UP * 0.2), run_time=0.25 if fast else 0.5)
                segs.add(seg)
                letters.add(t)
                i, j = ni, nj
            return segs, letters

        segs, letters = walk("aabab" + "a")
        t1 = T("최단 경로 = a 4개, b 2개의 나열", 30, INK).move_to(RIGHT * 3.5 + UP * 0.9)
        self.play(Write(t1))
        for mv in ["bbaaaa", "abaaba"]:
            self.play(FadeOut(segs), FadeOut(letters), run_time=0.3)
            segs, letters = walk(mv, fast=True)
        eq = label_box("6! ÷ (4! × 2!) = 15", w=5.6, h=0.95, size=38, fill=BLUE_SOFT, stroke=BLUE, color=BLUE).move_to(RIGHT * 3.5 + DOWN * 0.1)
        self.play(FadeIn(eq, scale=0.9))
        self.wait(1.0)

        # 각 점까지의 최단 경로 수 (왼쪽 + 아래쪽)
        self.play(FadeOut(segs), FadeOut(letters))
        t2 = T("각 점까지의 경로 수 = 왼쪽 + 아래쪽", 28, SUB).move_to(RIGHT * 3.5 + DOWN * 1.4)
        self.play(FadeIn(t2))
        from math import comb
        for d in range(7):
            labs = []
            for i in range(5):
                j = d - i
                if 0 <= j <= 2:
                    v = comb(i + j, i)
                    end = (i, j) == (4, 2)
                    bg = Circle(radius=0.3, fill_color=RED if end else WHITE, fill_opacity=1,
                                stroke_color=RED if end else BLUE, stroke_width=3).move_to(P(i, j))
                    labs.append(VGroup(bg, T(str(v), 24, WHITE if end else BLUE, BOLD).move_to(bg)))
            self.play(LaggedStart(*[GrowFromCenter(l) for l in labs], lag_ratio=0.1), run_time=0.6)
        self.play(Circumscribe(eq, color=RED))
        self.wait(1.5)
