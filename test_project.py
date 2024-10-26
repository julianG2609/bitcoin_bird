from game import Bitcoin, Pipe

def test_bitcoin_initial_position():
    bitcoin = Bitcoin()
    assert bitcoin.y == 300

def test_bitcoin_jump():
    bitcoin = Bitcoin()
    bitcoin.jump()
    assert bitcoin.velocity == bitcoin.lift

def test_pipe_initial_position():
    pipe = Pipe()
    assert pipe.x == 400
    assert 50 < pipe.top_height < 450
