import winsound
import threading

done = False

def music():
    global done
    while not done:
        print("game in progress")
        winsound.PlaySound('game_music.wav', winsound.SND_FILENAME)
    print("game ended")
    print("Bye!")

def end():
    ayo = input("Press enter to stop: ")
    if ayo == "":
        music_thread.join()
        global done
        done = True
        print("game end intiaition")
        winsound.PlaySound("game_over.wav", winsound.SND_FILENAME)

music_thread = threading.Thread(target=music, daemon=True)
music_thread.start()

end_thread = threading.Thread(target=end, daemon=False)
end_thread.start()