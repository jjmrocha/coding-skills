# Readable Code

Code is written once, changed a few times, and read hundreds of times. Readable code lets a reader understand it on the first pass, top to bottom, without jumping around or decoding.

Check the code you wrote against each item.

## 1. The top function reads like a summary

Each function works at one level of detail. The top function names its steps in the words of the problem, and the details live in smaller functions below it.

**Check:** could someone who knows the problem, but not the code, follow the top function?

```go
// Before: reading, parsing and saving all at one level
func importOrders(path string) error {
	f, err := os.Open(path)
	if err != nil {
		return err
	}
	defer f.Close()
	rows, err := csv.NewReader(f).ReadAll()
	if err != nil {
		return err
	}
	for _, row := range rows[1:] {
		qty, err := strconv.Atoi(row[2])
		if err != nil {
			return err
		}
		if _, err := db.Exec(insertOrder, row[0], row[1], qty); err != nil {
			return err
		}
	}
	return nil
}

// After
func importOrders(path string) error {
	rows, err := readCSV(path)
	if err != nil {
		return err
	}
	orders, err := parseOrders(rows)
	if err != nil {
		return err
	}
	return saveOrders(orders)
}
```

## 2. The file reads from top to bottom

A function sits above the functions it calls, so the reader meets the big picture first and the details later.

**Check:** reading the file from the top, do you meet each function's caller before the function itself?

## 3. Names say what a thing is, in the words of the problem

A name's length matches its scope: short for a few lines, longer for wide use. A function that changes something says so in its name.

**Check:** for each new name, could a reader guess what it holds or does without reading its definition?

```go
// Before
func handle(d []byte) []Item
func checkUser(u *User) bool // also updates u.LastSeen

// After
func parseInvoiceLines(csv []byte) []InvoiceLine
func touchLastSeen(u *User)
```

## 4. The code explains itself

An expression that needs a comment, or that does not fit on one line, gets a name: a variable or a small function.

**Check:** is there a comment that explains *what* a line does, or a line a reader must take apart to understand?

```go
// Before
results := control.Start(ctx, control.Limits{Requests: opts.Requests, Duration: opts.Duration, Workers: opts.Concurrency}, httpClient, tmpl, data)

// After
limits := control.Limits{Requests: opts.Requests, Duration: opts.Duration, Workers: opts.Concurrency}
results := control.Start(ctx, limits, httpClient, tmpl, data)
```

## 5. Related lines sit together

A variable is declared right before its first use. A blank line separates one step from the next, like paragraphs in text.

**Check:** is any variable declared well before its first use, or are two steps run together with no break?

## 6. Control flow stays flat

Handle errors and edge cases first and return early, so the main path runs down the left edge.

**Check:** is any code nested more than two levels deep?

```go
// Before
if user != nil {
	if user.Active {
		send(user)
	}
}

// After
if user == nil || !user.Active {
	return
}
send(user)
```

## 7. The code matches a plain description

Describe in a few plain sentences what the function does. The code follows those sentences, in the same order.

**Check:** write the sentences. Is there a line of code that belongs to no sentence, or a sentence the code spreads across several places?
