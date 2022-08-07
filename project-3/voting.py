# this is a voting programming we vote and see the results who win

nominee1 = input("Enter the name of first nominee: ")
nominee2 = input("Enter the name of second nominee: ")

# initially vote count for both team is zero
nm1_votes = 0
nm2_votes = 0

voter_id = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
no_of_voter = len(voter_id)

while True:
    if not voter_id:  # to check voter list is completed
        print("!!!!Voting session is over!!!!")
        if nm1_votes > nm2_votes:
            perc = (nm1_votes / no_of_voter) * 100
            print(f"{nominee1} is won with with {perc}% votes")
            break
        elif nm1_votes < nm2_votes:
            perc2 = (nm2_votes / no_of_voter) * 100
            print(f"{nominee2} is won with with {perc2}% votes")
            break
        else:
            print("Both have equal number of votes ")
            break

    voter = int(input("Enter your voter id: "))
    if voter in voter_id:
        print("You are a voter")
        voter_id.remove(voter)
        print("------------------------------------------")
        print(f"to give vote to {nominee1} Press 1")
        print(f"to give vote to {nominee2} Press 2")
        print("------------------------------------------")
        vote = int(input("Enter your vote: "))
        if vote == 1:
            nm1_votes += 1
            print(f"thanks for voting {nominee1}")
        elif vote == 2:
            nm2_votes += 1
            print(f"thanks for voting {nominee2}")
        elif vote > 2:
            print("check your pressed key")
        else:
            print("You are not a voter OR You have already voted")
