/**
 * An event emitter with the ability to cancel and defer events
 */
export class EventEmitter<Events extends object> {
  private events: {[K in keyof Events]: EventHandlers<Events[K]>};

  constructor(events: {[k in keyof Events]: true}) {
    this.events = Object.fromEntries(Object.keys(events).map(k => [k, []])) as any;
  }

  public on<E extends keyof Events>(name: E, handler: EventHandler<Events[E]>) {
    this.events[name].push(handler);
  }

  public emit<E extends keyof Events>(name: E, args: Events[E]): Events[E] & Event {
    let status: 'sync' | 'canceled' | 'deferred' = 'sync';
    let _block: () => void;

    const ev: Events[E] & Event = {
      ...args,
      cancelEvent() { status = 'canceled'; },
      deferEvent() {
        status = 'deferred';
        return () => {
          if (_block) {
            _block();
          }
        };
      },
      then(block) {
        if (status === 'sync') {
          block();
        } else if (status === 'deferred') {
          _block = block;
        }
      },
    };

    for (const handler of this.events[name]) {
      handler(ev);
    }

    return ev;
  }
}

export interface Event {
  /**
   * Cancel synchronous execution of the event
   */
  cancelEvent(): void;

  /**
   * Don't invoke the event code when 'then' is called, instead invoke it when the
   * returned function is called
   */
  deferEvent(): () => void;

  /**
   * Run the actual code if the event wasn't canceled, or will be invoked if it's deferred.
   */
  then(cb: () => void): void;
}

export type EventHandler<A> = (x: A & Event) => void;
export type EventHandlers<A> = Array<EventHandler<A>>;
