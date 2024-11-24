import click


class Selector:

    @staticmethod
    def select(options: list[str], max_items: int) -> str:

        click.clear()
        page = 0
        # epic oneliner
        show = lambda : click.echo(f"Page {page+1}.\nPress 'n' for next page, 'b' for previous, or Ctrl-C to quit.\n" +
                                   "\n".join(
                                       [f"{i}: {item}"
                                        for i, item in enumerate(
                                           options[page*max_items:(page+1)*max_items]
                                       )]
                                   ))
        show()

        max_page = len(options) // max_items
        if len(options) % max_items == 0:
            max_page -= 1

        while True:
            key = click.getchar()
            try:
                if int(key) in range(len(options)):
                    break
            except ValueError:
                pass
            if key == "n" and page < max_page:
                page += 1
                click.clear()
                show()
            elif key == "b" and page > 0:
                page -= 1
                click.clear()
                show()

        return options[page*max_items:(page+1)*max_items][int(key)]
