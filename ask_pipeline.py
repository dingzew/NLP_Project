import question1
import sys

def ask(line, N):
    q1 = question1.askWho(line)
    if q1 is not None and q1.strip():
        N -= 1
        print(q1)
    if N == 0:
      return N

    q1 = question1.askWhen(line)
    if q1 is not None and q1.strip():
        N -= 1
        print(q1)
    if N == 0:
      return N

    q1 = question1.askDoWhat(line)
    if q1 is not None and q1.strip():
        N -= 1
        print(q1)
    if N == 0:
      return N

    q1 = question1.askWhere(line)
    if q1 is not None and q1.strip():
        N -= 1
        print(q1)
    return N


if __name__ == "__main__":
    tests =[
       'Starbucks is doing very well lately.',
       'Overall, while it may seem there is already a Starbucks on every corner, Starbucks still has a lot of room to grow.',
       'They just began expansion into food products, which has been going quite well so far for them.',
       'I can attest that my own expenditure when going to Starbucks has increased, in lieu of these food products.',
       'Starbucks is also indeed expanding their number of stores as well.',
       'Starbucks still sees strong sales growth here in the united states, and intends to actually continue increasing this.',
       'Starbucks also has one of the more successful loyalty programs, which accounts for 30%  of all transactions being loyalty-program-based.',
       'As if news could not get any more positive for the company, Brazilian weather has become ideal for producing coffee beans.',
       'Brazil is the world\'s #1 coffee producer, the source of about 1/3rd of the entire world\'s supply!',
       'Given the dry weather, coffee farmers have amped up production, to take as much of an advantage as possible with the dry weather.',
       'Increase in supply... well you know the rules...',
    ]
    for line in tests:
        ask(line)